import warnings
from langchain.document_loaders import HuggingFaceDatasetLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from langchain import HuggingFacePipeline
from langchain.chains import RetrievalQA
import requests
import os
from flask import Flask, request, jsonify
from langchain.schema import Document

# Directory constants
MODEL_DIR = 'models'
EMBEDDINGS_DIR = os.path.join(MODEL_DIR, 'embeddings')
QA_MODEL_DIR = os.path.join(MODEL_DIR, 'qa')
DATA_DIR = 'data'
WP_POSTS_DIR = os.path.join(DATA_DIR, 'wordpress_posts')
UTILS_DIR = 'utils'

# Create directories if they don't exist
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
os.makedirs(QA_MODEL_DIR, exist_ok=True)
os.makedirs(WP_POSTS_DIR, exist_ok=True)
os.makedirs(UTILS_DIR, exist_ok=True)

# Constants for models and dataset
DATASET_NAME = "databricks/databricks-dolly-15k"
PAGE_CONTENT_COLUMN = "context"
EMBEDDING_MODEL_PATH = "sentence-transformers/all-MiniLM-l6-v2"
QA_MODEL_NAME = "Intel/dynamic_tinybert"
BASE_URL = "https://techcrunch.com"

# Initialize Flask app
app = Flask(__name__)

# Load dataset and split it into manageable chunks
loader = HuggingFaceDatasetLoader(DATASET_NAME, PAGE_CONTENT_COLUMN)
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(data)

# Set up embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_PATH, model_kwargs={'device': 'cpu'}, encode_kwargs={'normalize_embeddings': False})
db = FAISS.from_documents(docs, embeddings)

# Set up question-answering model
tokenizer = AutoTokenizer.from_pretrained(QA_MODEL_NAME)
model = AutoModelForQuestionAnswering.from_pretrained(QA_MODEL_NAME)
question_answerer = pipeline("question-answering", model=model, tokenizer=tokenizer, return_tensors='pt')
llm = HuggingFacePipeline(pipeline=question_answerer, model_kwargs={"temperature": 0.7, "max_length": 512})

# Set up retriever and QA pipeline
retriever = db.as_retriever(search_kwargs={"k": 4})
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="refine", retriever=retriever, return_source_documents=False)

# Define function to fetch posts from a WordPress site
def fetch_wordpress_posts(base_url, count=15, post_type='posts'):
    url = f"{base_url}/wp-json/wp/v2/{post_type}"
    params = {'per_page': count}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Load WordPress posts and add to vector store
wp_data = fetch_wordpress_posts(BASE_URL)
wp_docs = [Document(page_content=doc['content']['rendered']) for doc in wp_data]
wp_docs_split = text_splitter.split_documents(wp_docs)
db.add_documents(wp_docs_split)

# Define function to process user queries
def answer_question(final_question):
    wp_search_docs = db.similarity_search(final_question)
    context = " ".join([doc.page_content for doc in wp_search_docs])
    qa_input = {"question": final_question, "context": context}
    final_answer = question_answerer(qa_input)
    return final_answer['answer']

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get('query')
    answer = answer_question(user_query)
    return jsonify(response=answer)

@app.route('/retrievee', methods=['POST'])
def retrievee():
    query = request.json.get('query')
    wp_search_docs = db.similarity_search(query)
    retrieved_docs = [{"content": doc.page_content} for doc in wp_search_docs]
    return jsonify(docs=retrieved_docs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

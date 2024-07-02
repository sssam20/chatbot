import { useState } from 'react';
import axios from 'axios';

export default function Home() {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState('');

    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    const handleSendQuery = async () => {
        try {
            const res = await axios.post('/api/chatbot', { query });
            setResponse(res.data.response);
        } catch (error) {
            setResponse('Error communicating with the server.');
        }
    };

    return (
        <div>
            <h1>Chatbot</h1>
            <div>
                <input
                    type="text"
                    value={query}
                    onChange={handleQueryChange}
                    placeholder="Type your message here..."
                />
                <button onClick={handleSendQuery}>Send</button>
            </div>
            <div>
                <h2>Response:</h2>
                <p>{response}</p>
            </div>
        </div>
    );
}

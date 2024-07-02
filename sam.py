import os

# Define the directory structure
directory_structure = {
    'backend': {
        'files': ['app.py', 'requirements.txt', 'Dockerfile', '.env']
    },
    'frontend': {
        'files': ['.gitignore', 'package.json', 'vercel.json', 'next.config.js'],
        'directories': {
            'pages': {
                'directories': {
                    'api': {
                        'files': ['chatbot.js']
                    }
                },
                'files': ['index.js']
            },
            'public': {},  # Placeholder for public assets if needed
            'styles': {
                'files': ['globals.css']
            }
        }
    },
    'wordpress-plugin': {
        'files': ['my-chatbot-plugin.php'],
        'directories': {
            'assets': {
                'directories': {
                    'css': {
                        'files': ['chatbot.css']
                    },
                    'js': {
                        'files': ['chatbot.js']
                    }
                }
            }
        }
    },
    '.gitignore': {}  # Placeholder for a root .gitignore file if needed
}

# Function to create directory structure recursively
def create_directory_structure(base_path, structure):
    for name, contents in structure.items():
        path = os.path.join(base_path, name)
        os.makedirs(path, exist_ok=True)
        if 'files' in contents:
            for file in contents['files']:
                with open(os.path.join(path, file), 'w') as f:
                    pass  # Create an empty file
        if 'directories' in contents:
            create_directory_structure(path, contents['directories'])

# Specify the base directory where the structure should be created
base_directory = r'C:\Users\Sameer Sonwane\Videos\project\rag-chatbot-wordpress'

# Create the directory structure
create_directory_structure(base_directory, directory_structure)

print("Directory structure created successfully.")

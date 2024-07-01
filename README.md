
# Parrot PDF Chat 🦜

Parrot PDF Chat is an intelligent chatbot application that allows users to ask questions based on the content of uploaded PDF documents. The application uses Django for the backend, Langchain for natural language processing, and the Mistral 7B model for generating responses.

## Features

- Upload PDF documents to be used as the knowledge base.
- Ask questions and receive answers based on the content of the uploaded PDFs.
- Maintains conversation history using Redis.
- User-friendly interface for chatting with the bot.

## Technologies Used

- **Django**: Web framework for the backend.
- **Langchain**: Natural language processing and conversational AI.
- **Mistral 7B**: A local language model used for generating responses.
- **Redis**: Used for maintaining conversation history.

## Installation

1. **Clone the repository**
   \`\`\`sh
   git clone <repository_url>
   cd parrot-pdf-chat
   \`\`\`

2. **Create a virtual environment**
   \`\`\`sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   \`\`\`

3. **Install the dependencies**
   \`\`\`sh
   pip install -r requirements.txt
   \`\`\`

4. **Setup Redis**
   - Install Redis and ensure it's running on your machine.
   - Update the Redis configuration in your Django settings if necessary.

5. **Run migrations**
   \`\`\`sh
   python manage.py migrate
   \`\`\`

6. **Start the Django development server**
   \`\`\`sh
   python manage.py runserver
   \`\`\`

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`

## Usage

1. **Upload PDF documents**
   - Navigate to the upload page and upload your PDF documents.

2. **Ask questions**
   - Use the chat interface to ask questions based on the content of the uploaded PDFs.

## License

This project is licensed under the MIT License.


## UI
![0630(1)_Moment](https://github.com/Mu5alaf/Parrot-Chatbot/assets/109148687/f8e85312-f16b-4502-907f-dbd049e6eb93)



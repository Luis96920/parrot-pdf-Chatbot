document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const chatContainer = document.querySelector('.chat-container');
    const newConversationBtn = document.getElementById('new-conversation-btn');
    const lastConversation = document.querySelector('conversation-text');
    let chat_history = JSON.parse(localStorage.getItem('chat_history')) || [];

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    sidebarToggle.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
        if (sidebar.classList.contains('collapsed')) {
            chatContainer.style.width = '96%';
            chatContainer.style.marginLeft = '3%';
        } else {
            chatContainer.style.width = 'calc(100% - 300px)';
            chatContainer.style.marginLeft = '300px';
        }
    });

    newConversationBtn.addEventListener('click', function () {
        if (lastConversation) {
            lastConversation.textContent = "New Conversation Started!";
        }
        chat_history = [];
        chatBox.innerHTML = ''; // Clear chat box
        localStorage.removeItem('chat_history');
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message !== '') {
            appendMessage('user', `You: ${message}`);
            getResponse(message);
            userInput.value = '';
        }
    }

    function appendMessage(sender, message) {
        const messageContainer = document.createElement('div');
        const messageParagraph = document.createElement('p');
        messageParagraph.textContent = message;

        if (sender === 'user') {
            messageContainer.classList.add('message', 'user-message');
        } else {
            messageContainer.classList.add('message', 'agent-message');
        }

        messageContainer.appendChild(messageParagraph);
        chatBox.appendChild(messageContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function getResponse(message) {
        fetch('/Home/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ question: message, chat_history: chat_history })
        })
            .then(response => response.json())
            .then(data => {
                if (data.answer) {
                    chat_history.push({ user: message, agent: data.answer });
                    appendMessage('agent', `Agent: ${data.answer}`);
                    localStorage.setItem('chat_history', JSON.stringify(chat_history));
                } else {
                    appendMessage('agent', `Error Append: ${data.error}`);
                }
            })
            .catch(error => {
                appendMessage('agent', `Error Catch: ${error.message}`);
            });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function loadChatHistory() {
        chat_history.forEach(entry => {
            appendMessage('user', `You: ${entry.user}`);
            appendMessage('agent', `Agent: ${entry.agent}`);
        });
    }
    loadChatHistory();
});

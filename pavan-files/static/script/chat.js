function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    const question = userInput.value.trim();

    if (userInput.value.trim() !== "") {
        const userMessage = document.createElement('div');
        userMessage.textContent = userInput.value;
        userMessage.style.padding = '10px';
        userMessage.style.margin = '10px 0';
        userMessage.style.background = '#007bff';
        userMessage.style.color = 'white';
        userMessage.style.borderRadius = '4px';
        userMessage.style.alignSelf = 'flex-end';

        chatMessages.appendChild(userMessage);
        userInput.value = '';
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Simulate AI response

        const data = {};
        data['question'] = question;

        fetch('/chat_with_ai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => response.json()).then(data => {
            console.log(data);
            const aiMessage = document.createElement('div');
            aiMessage.innerHTML = data.answer;
            aiMessage.style.padding = '10px';
            aiMessage.style.margin = '10px 0';
            aiMessage.style.background = '#ddd';
            aiMessage.style.borderRadius = '4px';
            aiMessage.style.alignSelf = 'flex-start';

            chatMessages.appendChild(aiMessage);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }).error(error => {
            console.error(error);
        });

    }
}
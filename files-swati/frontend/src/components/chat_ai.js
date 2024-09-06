import React, { useState } from 'react';
import "./styles/chat_ai.css";
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook

const Chatai = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const navigate = useNavigate(); // Initialize the navigate function

  const handleSubmit = (e) => {
    e.preventDefault();

    const data = { question: input };
    console.log(data);

    fetch('http://127.0.0.1:5000/chat_with_ai', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        const response = data.answer;
        const newMessage = {
          text: input,
          sender: "self",
          time: new Date().toLocaleTimeString(),
        };

        setMessages((prevMessages) => [...prevMessages, newMessage]);

        const aiMessage = {
          text: response,
          sender: "other",
          time: new Date().toLocaleTimeString(),
        };

        setMessages((prevMessages) => [...prevMessages, aiMessage]);
        setInput("");
      })
      .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
      });
  };

  const handleChatboxRedirect = () => {
    navigate("/chatbox"); // Navigate to the /chatbox page
  };

  return (
      <div className="chat-container">
          
        <div className='poipoi'>
        <h1>Ask Your Doubts </h1>
        <button className="redirect-chatbutton" onClick={handleChatboxRedirect}>Go to Chatbox</button>
        </div>
          
      <ul className="chat-messages">
        {messages.map((msg, index) => (
          <li key={index} className={`message ${msg.sender}`}>
            <div className={`message-content ${msg.sender}`} dangerouslySetInnerHTML={{ __html: msg.text }}>
            </div>
            <div className="message-time">
              {msg.time}
            </div>
          </li>
        ))}
      </ul>
      <form className="input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          autoComplete="off"
        />
        <button type="submit">Send</button>
      </form>
      {/* Add redirect button here */}
      
    </div>
  );
};

export default Chatai;

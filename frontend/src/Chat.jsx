import React, { useState } from 'react';
import { FiSend } from 'react-icons/fi';
import { useParams, useLocation } from 'react-router-dom';
import './App.css';

const ChatInterface = () => {
  const { docId } = useParams();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const location = useLocation();

  const filename = location.state?.filename || 'demo.pdf';

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessage = {
      sender: 'user',
      text: input,
    };

    setMessages([...messages, newMessage]);
    setInput('');
    setLoading(true);
    const typingMessage = { sender: 'ai', text: 'AI is typing...' };
    setMessages((prev) => [...prev, typingMessage]);

    // Mock AI response (you'll replace this with backend call)
    try {
      const response = await fetch('http://127.0.0.1:8000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: input }),
      });

      if (!response.ok) {
        throw new Error('Failed to get the Response from the server');
      }
      const data = await response.json();
      const aiMessage = {
        sender: 'AI',
        text: data.answerit || 'No response recieved',
      };

      setMessages((prev) => [...prev.slice(0, -1), aiMessage]);
    } catch (error) {
      console.error('Error during /ask', error);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'AI',
          text: 'Error with the message' + error.message,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='flex flex-col h-screen bg-gray-100'>
      {/* Header */}
      <div className='p-4 bg-white shadow flex justify-between items-center'>
        <h1 className='text-xl font-bold text-gray-800'>PDF_Talk</h1>
        <div className='text-sm text-gray-500'>{filename}</div>
      </div>

      {/* Chat Area */}
      <div className='flex-1 overflow-y-auto p-4 space-y-4'>
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`max-w-xl px-4 py-2 rounded-lg ${
              msg.sender === 'user'
                ? 'bg-purple-100 self-end ml-auto text-right'
                : 'bg-green-100 self-start'
            }`}
          >
            <p className='text-gray-800'>{msg.text}</p>
          </div>
        ))}
      </div>

      {/* Input Bar */}
      <div className='p-4 bg-white shadow flex items-center gap-3'>
        <input
          type='text'
          placeholder='Send a message...'
          className='flex-1 p-3 border border-gray-300 rounded-lg outline-none'
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        />
        <button
          onClick={handleSend}
          className='bg-purple-600 text-white p-3 rounded-lg hover:bg-purple-700'
        >
          <FiSend size={20} />
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;

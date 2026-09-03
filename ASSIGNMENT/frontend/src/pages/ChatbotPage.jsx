import React, { useState } from 'react';
import { api } from '../services/api';

export default function ChatbotPage({ setCurrentPage, setSelectedTicketId }) {
  const [messages, setMessages] = useState([
    { sender: 'assistant', text: 'Hello! I am the Intelligent Campus Helpdesk Assistant. How can I help you with facility fault diagnosis today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(`session_${Date.now()}`);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { sender: 'user', text: userMsg }]);
    setLoading(true);

    try {
      const res = await api.sendChatMessage({ message: userMsg, session_id: sessionId });
      setMessages(prev => [...prev, { sender: 'assistant', text: res.reply, ticket: res.ticket_created, diagnosis: res.diagnosis_result }]);

      if (res.ticket_created) {
        // Auto notification or option to jump to ticket details
      }
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'assistant', text: 'Sorry, an error occurred while processing your request.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '850px', margin: '0 auto' }}>
      <div style={{ marginBottom: '1.25rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>Conversational AI Helpdesk Assistant</h2>
        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
          Report AC, Projector, Wi-Fi, or Equipment issues interactively. The AI will ask clarifying questions via backward chaining logic.
        </p>
      </div>

      <div className="chat-window">
        <div className="chat-messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-bubble ${msg.sender === 'user' ? 'message-user' : 'message-assistant'}`}>
              <div>{msg.text}</div>

              {msg.ticket && (
                <div style={{ marginTop: '0.75rem', paddingTop: '0.5rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                  <div style={{ fontWeight: 600, color: '#34d399' }}>✅ Ticket Created: {msg.ticket.ticket_number}</div>
                  <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Status: {msg.ticket.status} | Assigned Staff: #{msg.ticket.assigned_staff_id}</div>
                  <button
                    className="btn btn-secondary"
                    style={{ marginTop: '0.5rem', padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
                    onClick={() => {
                      setSelectedTicketId(msg.ticket.id);
                      setCurrentPage('ticket_details');
                    }}
                  >
                    View Full AI Proof Trace
                  </button>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message-bubble message-assistant" style={{ fontStyle: 'italic', color: '#94a3b8' }}>
              AI Assistant is thinking & checking Knowledge Base...
            </div>
          )}
        </div>

        <form onSubmit={handleSend} className="chat-input-row">
          <input
            type="text"
            placeholder="Type your message (e.g., 'The AC in CSE Lab 2 is not cooling' or 'Where is my ticket?')..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button type="submit" className="btn btn-primary" disabled={loading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

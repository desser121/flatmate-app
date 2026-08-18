import { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../services/api';
import type { Message, User } from '../types';

export default function ChatPage() {
  const navigate = useNavigate();
  const { matchId } = useParams<{ matchId: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [otherUser, setOtherUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const loadConversation = async () => {
      try {
        const convRes = await api.get('/chat/');
        const convs = convRes.data.results || convRes.data || [];
        const conv = convs.find((c: any) => c.match === matchId);
        if (conv) {
          setConversationId(conv.id);
          setOtherUser(conv.other_user);
          const msgRes = await api.get(`/chat/${conv.id}/messages/`);
          setMessages(msgRes.data.results || msgRes.data || []);
        }
      } catch {
      } finally {
        setLoading(false);
      }
    };
    if (matchId) loadConversation();
  }, [matchId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!newMessage.trim() || !conversationId) return;
    const text = newMessage.trim();
    setNewMessage('');

    try {
      const res = await api.post(`/chat/${conversationId}/messages/create/`, {
        content: text,
        message_type: 'text',
      });
      setMessages(prev => [...prev, res.data]);
    } catch {
      setNewMessage(text);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (loading) {
    return (
      <div className="chat-page">
        <div className="loading"><div className="spinner" /></div>
      </div>
    );
  }

  return (
    <div className="chat-page">
      <div className="chat-header">
        <button className="chat-back" onClick={() => navigate(-1)}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M15 18l-6-6 6-6" />
          </svg>
        </button>
        <div className="match-avatar-placeholder" style={{ width: 36, height: 36, fontSize: 14 }}>
          {otherUser?.name?.charAt(0) || '?'}
        </div>
        <div>
          <div style={{ fontWeight: 600, fontSize: 15 }}>{otherUser?.name}</div>
          <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>{otherUser?.city}</div>
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-state" style={{ paddingTop: 40 }}>
            <p>Начни общение первым!</p>
          </div>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`message ${msg.author_name === 'me' || msg.author === localStorage.getItem('user_id') ? 'sent' : 'received'}`}
          >
            <div>{msg.content}</div>
            <div className="message-time">
              {new Date(msg.created_at).toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <input
          type="text"
          placeholder="Сообщение..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={handleSend} disabled={!newMessage.trim()}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
    </div>
  );
}

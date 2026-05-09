'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import styles from '../../styles/messages.module.css';

interface Conversation {
  id: number;
  other_user_id: number;
  other_user_name: string;
  last_message: string;
  last_message_time: string;
  unread_count: number;
}

interface Message {
  id: number;
  sender_id: number;
  receiver_id: number;
  content: string;
  created_at: string;
  sender_name: string;
}

export default function MessagesPage() {
  const router = useRouter();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [currentUserId, setCurrentUserId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');

    if (!token || !userId) {
      router.push('/login');
      return;
    }

    setCurrentUserId(parseInt(userId));
    fetchConversations(token);
  }, [router]);

  useEffect(() => {
    if (selectedConversation) {
      const token = localStorage.getItem('token');
      if (token) {
        fetchMessages(token, selectedConversation.id);
      }
    }
  }, [selectedConversation]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchConversations = async (token: string) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/messages/conversations`, { headers });
      setConversations(response.data);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMessages = async (token: string, conversationId: number) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/messages/conversation/${conversationId}`,
        { headers }
      );
      setMessages(response.data);

      // Mark messages as read
      await axios.put(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/messages/conversation/${conversationId}/mark-read`,
        {},
        { headers }
      );

      // Refresh conversations to update unread count
      fetchConversations(token);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newMessage.trim() || !selectedConversation) return;

    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.post(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/messages/send`,
        {
          receiver_id: selectedConversation.other_user_id,
          content: newMessage,
        },
        { headers }
      );

      setNewMessage('');
      fetchMessages(token!, selectedConversation.id);
      fetchConversations(token!);
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message');
    }
  };

  const getInitials = (name: string) => {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  const formatTime = (dateString: string) => {
    // Parse the date string and ensure it's treated as UTC if it doesn't have timezone info
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      // Use user's local timezone
      return date.toLocaleTimeString(undefined, {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      });
    } else if (diffInHours < 48) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
    }
  };

  if (loading) {
    return <div className="loading">Loading messages...</div>;
  }

  return (
    <div className={styles['messages-container']}>
          <button
            className={styles['back-button']}
            onClick={() => router.push('/dashboard')}
          >
            ← Back to Dashboard
          </button>
      <div className={styles['messages-content-wrapper']}>
        <div className={styles['page-header']}>
          <h1>Messages</h1>
        </div>

        <div className={styles['messages-layout']}>
        <div className={styles['conversations-panel']}>
          <div className={styles['conversations-header']}>
            <h2>Conversations</h2>
          </div>

          <div className={styles['conversations-list']}>
            {conversations.length > 0 ? (
              conversations.map((conversation) => (
                <div
                  key={conversation.id}
                  className={`${styles['conversation-item']} ${
                    selectedConversation?.id === conversation.id ? styles.active : ''
                  }`}
                  onClick={() => setSelectedConversation(conversation)}
                >
                  <div className={styles['conversation-name']}>
                    {conversation.other_user_name}
                    {conversation.unread_count > 0 && (
                      <span className={styles['unread-badge']}>
                        {conversation.unread_count}
                      </span>
                    )}
                  </div>
                  <div className={styles['conversation-preview']}>
                    {conversation.last_message}
                  </div>
                  <div className={styles['conversation-time']}>
                    {formatTime(conversation.last_message_time)}
                  </div>
                </div>
              ))
            ) : (
              <div className={styles['no-conversations']}>
                <p>No conversations yet</p>
                <p style={{ fontSize: '14px', marginTop: '10px' }}>
                  Start a conversation by messaging someone from the Collaboration page
                </p>
              </div>
            )}
          </div>
        </div>

        <div className={styles['chat-panel']}>
          {selectedConversation ? (
            <>
              <div className={styles['chat-header']}>
                <h2>{selectedConversation.other_user_name}</h2>
              </div>

              <div className={styles['chat-messages']}>
                {messages.map((message) => {
                  const isSent = message.sender_id === currentUserId;
                  return (
                    <div
                      key={message.id}
                      className={`${styles.message} ${isSent ? styles.sent : styles.received}`}
                    >
                      <div className={styles['message-avatar']}>
                        {getInitials(isSent ? 'You' : message.sender_name)}
                      </div>
                      <div className={styles['message-content']}>
                        <div className={styles['message-bubble']}>
                          {message.content}
                        </div>
                        <div className={styles['message-time']}>
                          {formatTime(message.created_at)}
                        </div>
                      </div>
                    </div>
                  );
                })}
                <div ref={messagesEndRef} />
              </div>

              <div className={styles['chat-input-container']}>
                <form onSubmit={handleSendMessage} className={styles['chat-input-form']}>
                  <input
                    type="text"
                    className={styles['chat-input']}
                    placeholder="Type a message..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                  />
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={!newMessage.trim()}
                  >
                    Send
                  </button>
                </form>
              </div>
            </>
          ) : (
            <div className={styles['empty-chat']}>
              <div>
                <div className={styles['empty-chat-icon']}>💬</div>
                <h2>Select a conversation</h2>
                <p>Choose a conversation from the list to start messaging</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
    </div>
  );
}


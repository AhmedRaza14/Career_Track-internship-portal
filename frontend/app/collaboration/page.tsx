'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import styles from '../../styles/collaboration.module.css';

interface CollaborationPost {
  id: number;
  title: string;
  description: string;
  required_skills: string;
  author_id: number;
  author_name: string;
  created_at: string;
}

export default function CollaborationPage() {
  const router = useRouter();
  const [posts, setPosts] = useState<CollaborationPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [currentUserId, setCurrentUserId] = useState<number | null>(null);
  const [selectedPost, setSelectedPost] = useState<CollaborationPost | null>(null);
  const [newPost, setNewPost] = useState({
    title: '',
    description: '',
    required_skills: '',
  });
  const [editPost, setEditPost] = useState({
    title: '',
    description: '',
    required_skills: '',
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');

    if (!token || !userId) {
      router.push('/login');
      return;
    }

    setCurrentUserId(parseInt(userId));
    fetchPosts(token);
  }, [router]);

  const fetchPosts = async (token: string) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/collaboration`, { headers });
      setPosts(response.data);
    } catch (error) {
      console.error('Error fetching collaboration posts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePost = async () => {
    if (!newPost.title.trim() || !newPost.description.trim()) {
      alert('Please fill in all required fields');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/collaboration/create`, newPost, { headers });

      setShowCreateModal(false);
      setNewPost({ title: '', description: '', required_skills: '' });
      fetchPosts(token!);
    } catch (error) {
      console.error('Error creating post:', error);
      alert('Failed to create collaboration post');
    }
  };

  const handleEditPost = async () => {
    if (!editPost.title.trim() || !editPost.description.trim()) {
      alert('Please fill in all required fields');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.put(`${process.env.NEXT_PUBLIC_API_BASE_URL}/collaboration/${selectedPost?.id}`, editPost, { headers });

      setShowEditModal(false);
      setSelectedPost(null);
      setEditPost({ title: '', description: '', required_skills: '' });
      fetchPosts(token!);
    } catch (error) {
      console.error('Error updating post:', error);
      alert('Failed to update collaboration post');
    }
  };

  const handleDeletePost = async (postId: number) => {
    if (!confirm('Are you sure you want to delete this collaboration post?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.delete(`${process.env.NEXT_PUBLIC_API_BASE_URL}/collaboration/${postId}`, { headers });

      fetchPosts(token!);
    } catch (error) {
      console.error('Error deleting post:', error);
      alert('Failed to delete collaboration post');
    }
  };

  const openEditModal = (post: CollaborationPost) => {
    setSelectedPost(post);
    setEditPost({
      title: post.title,
      description: post.description,
      required_skills: post.required_skills || '',
    });
    setShowEditModal(true);
  };

  const handleMessageUser = async (userId: number, userName: string, postTitle: string) => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      // Create or get conversation with context about the collaboration post
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/messages/send`,
        {
          receiver_id: userId,
          content: `Hi ${userName}, I'm interested in collaborating on your project: "${postTitle}". Let's discuss!`,
        },
        { headers }
      );

      router.push('/messages');
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Failed to send message');
    }
  };

  if (loading) {
    return <div className="loading">Loading collaboration posts...</div>;
  }

  const myPosts = posts.filter(post => post.author_id === currentUserId);
  const otherPosts = posts.filter(post => post.author_id !== currentUserId);

  return (
    <div className={styles['collab-container']}>
        <div className={styles['page-header-with-back']}>
          <button
            className={styles['back-button']}
            onClick={() => router.push('/dashboard')}
          >
            ← Back to Dashboard
          </button>
        </div>
      <div className={styles['collab-content-wrapper']}>

        <div className={styles['collab-header']}>
        <div>
          <h1>Collaboration</h1>
          <p>Find students to collaborate on projects</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
          Create Post
        </button>
      </div>

      {/* My Collaboration Posts */}
      {myPosts.length > 0 && (
        <div style={{ marginBottom: '40px' }}>
          <h2 style={{ marginBottom: '20px', fontSize: '1.5rem' }}>My Collaboration Posts</h2>
          <div className={styles['collab-grid']}>
            {myPosts.map((post) => (
              <div key={post.id} className={styles['collab-card']}>
                <div className={styles['collab-card-header']}>
                  <h2 className={styles['collab-title']}>{post.title}</h2>
                  <div className={styles['collab-author']}>
                    <span>👤</span>
                    <span>Posted by You</span>
                  </div>
                </div>

                <p className={styles['collab-description']}>{post.description}</p>

                {post.required_skills && (
                  <div className={styles['collab-skills']}>
                    {post.required_skills.split(',').map((skill, idx) => (
                      <span key={idx} className={styles['collab-skill-tag']}>
                        {skill.trim()}
                      </span>
                    ))}
                  </div>
                )}

                <div className={styles['collab-footer']}>
                  <span className={styles['collab-date']}>
                    {new Date(post.created_at).toLocaleDateString()}
                  </span>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                      className="btn btn-outline"
                      onClick={() => openEditModal(post)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDeletePost(post.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* All Collaboration Posts (excluding mine) */}
      <div>
        <h2 style={{ marginBottom: '20px', fontSize: '1.5rem' }}>All Collaboration Posts</h2>
        {otherPosts.length > 0 ? (
          <div className={styles['collab-grid']}>
            {otherPosts.map((post) => (
              <div key={post.id} className={styles['collab-card']}>
                <div className={styles['collab-card-header']}>
                  <h2 className={styles['collab-title']}>{post.title}</h2>
                  <div className={styles['collab-author']}>
                    <span>👤</span>
                    <span>Posted by {post.author_name}</span>
                  </div>
                </div>

                <p className={styles['collab-description']}>{post.description}</p>

                {post.required_skills && (
                  <div className={styles['collab-skills']}>
                    {post.required_skills.split(',').map((skill, idx) => (
                      <span key={idx} className={styles['collab-skill-tag']}>
                        {skill.trim()}
                      </span>
                    ))}
                  </div>
                )}

                <div className={styles['collab-footer']}>
                  <span className={styles['collab-date']}>
                    {new Date(post.created_at).toLocaleDateString()}
                  </span>
                  <button
                    className="btn btn-primary"
                    onClick={() => handleMessageUser(post.author_id, post.author_name, post.title)}
                  >
                    Message
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className={styles['empty-state']}>
            <div className={styles['empty-state-icon']}>🤝</div>
            <h2>No collaboration posts yet</h2>
            <p>Be the first to create a collaboration post!</p>
          </div>
        )}
      </div>

      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Create Collaboration Post</h2>
              <button className="close-btn" onClick={() => setShowCreateModal(false)}>×</button>
            </div>
            <div className="form-group">
              <label className="form-label">Project Title</label>
              <input
                type="text"
                className="form-input"
                value={newPost.title}
                onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
                placeholder="e.g., Looking for React developer"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Description</label>
              <textarea
                className="form-textarea"
                value={newPost.description}
                onChange={(e) => setNewPost({ ...newPost, description: e.target.value })}
                placeholder="Describe your project and what you're looking for..."
              />
            </div>
            <div className="form-group">
              <label className="form-label">Skills Needed (comma-separated)</label>
              <input
                type="text"
                className="form-input"
                value={newPost.required_skills}
                onChange={(e) => setNewPost({ ...newPost, required_skills: e.target.value })}
                placeholder="e.g., React, Node.js, MongoDB"
              />
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleCreatePost}>
              Create Post
            </button>
          </div>
        </div>
      )}

      {showEditModal && (
        <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Edit Collaboration Post</h2>
              <button className="close-btn" onClick={() => setShowEditModal(false)}>×</button>
            </div>
            <div className="form-group">
              <label className="form-label">Project Title</label>
              <input
                type="text"
                className="form-input"
                value={editPost.title}
                onChange={(e) => setEditPost({ ...editPost, title: e.target.value })}
                placeholder="e.g., Looking for React developer"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Description</label>
              <textarea
                className="form-textarea"
                value={editPost.description}
                onChange={(e) => setEditPost({ ...editPost, description: e.target.value })}
                placeholder="Describe your project and what you're looking for..."
              />
            </div>
            <div className="form-group">
              <label className="form-label">Skills Needed (comma-separated)</label>
              <input
                type="text"
                className="form-input"
                value={editPost.required_skills}
                onChange={(e) => setEditPost({ ...editPost, required_skills: e.target.value })}
                placeholder="e.g., React, Node.js, MongoDB"
              />
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleEditPost}>
              Update Post
            </button>
          </div>
        </div>
      )}
    </div>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import styles from '../../styles/dashboard.module.css';

export default function DashboardPage() {
  const router = useRouter();
  const [stats, setStats] = useState({
    applications: 0,
    collaborations: 0,
    messages: 0,
  });
  const [loading, setLoading] = useState(true);
  const [role, setRole] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('role');

    if (!token) {
      router.push('/login');
      return;
    }

    if (userRole) {
      setRole(userRole);
    }

    fetchDashboardStats(token);
  }, [router]);

  const fetchDashboardStats = async (token: string) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };

      // Fetch applications count
      const appsResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/applications/my`, {
        headers,
      });

      // Fetch collaboration posts count
      const collabResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/collaboration`, {
        headers,
      });

      // Fetch conversations count
      const convResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/messages/conversations`, {
        headers,
      });

      setStats({
        applications: appsResponse.data.length || 0,
        collaborations: collabResponse.data.length || 0,
        messages: convResponse.data.length || 0,
      });
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div>
      <div className={styles['page-header']}>
        <h1>Dashboard</h1>
        <p>Welcome back! Here's your overview</p>
      </div>

      <div className={styles['stats-grid']}>
        <div className={styles['stat-card']}>
          <div className={styles['stat-header']}>
            <span className={styles['stat-title']}>
              {role === 'student' ? 'Job Applications' : 'Posted Jobs'}
            </span>
            <span className={styles['stat-icon']}>📝</span>
          </div>
          <div className={styles['stat-value']}>{stats.applications}</div>
        </div>

        <div className={styles['stat-card']}>
          <div className={styles['stat-header']}>
            <span className={styles['stat-title']}>Collaboration Posts</span>
            <span className={styles['stat-icon']}>🤝</span>
          </div>
          <div className={styles['stat-value']}>{stats.collaborations}</div>
        </div>

        <div className={styles['stat-card']}>
          <div className={styles['stat-header']}>
            <span className={styles['stat-title']}>Messages</span>
            <span className={styles['stat-icon']}>💬</span>
          </div>
          <div className={styles['stat-value']}>{stats.messages}</div>
        </div>
      </div>

      <div className="card">
        <h2 style={{ marginBottom: '15px' }}>Quick Actions</h2>
        <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
          {role === 'student' && (
            <>
              <button
                onClick={() => router.push('/profile')}
                className="btn btn-primary"
              >
                Update Profile
              </button>
              <button
                onClick={() => router.push('/jobs')}
                className="btn btn-outline"
              >
                Browse Jobs
              </button>
              <button
                onClick={() => router.push('/collaboration')}
                className="btn btn-outline"
              >
                Find Collaborators
              </button>
            </>
          )}
          {role === 'recruiter' && (
            <>
              <button
                onClick={() => router.push('/jobs')}
                className="btn btn-primary"
              >
                Post a Job
              </button>
              <button
                onClick={() => router.push('/messages')}
                className="btn btn-outline"
              >
                View Messages
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

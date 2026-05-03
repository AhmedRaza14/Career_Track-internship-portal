'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import styles from '../../styles/role.module.css';

export default function SelectRolePage() {
  const router = useRouter();
  const [selectedRole, setSelectedRole] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRoleSubmit = async () => {
    if (!selectedRole) {
      setError('Please select a role');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const tempToken = localStorage.getItem('temp_token');

      if (!tempToken) {
        setError('Session expired. Please login again.');
        router.push('/login');
        return;
      }

      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/google/complete`,
        { role: selectedRole },
        {
          headers: {
            'Authorization': `Bearer ${tempToken}`
          }
        }
      );

      const { access_token, role, user_id } = response.data;

      localStorage.setItem('token', access_token);
      localStorage.setItem('role', role);
      localStorage.setItem('user_id', user_id);
      localStorage.removeItem('temp_token');

      router.push('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to complete registration');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles['role-container']}>
      <div className={styles['role-card']}>
        <div className={styles['role-header']}>
          <h1>Welcome to CareerTrack!</h1>
          <p>Please select your role to continue</p>
        </div>

        <div className={styles['role-options']}>
          <div
            className={`${styles['role-option']} ${selectedRole === 'student' ? styles.selected : ''}`}
            onClick={() => setSelectedRole('student')}
          >
            <div className={styles['role-icon']}>🎓</div>
            <h3>Student</h3>
            <p>Looking for jobs and collaboration opportunities</p>
          </div>

          <div
            className={`${styles['role-option']} ${selectedRole === 'recruiter' ? styles.selected : ''}`}
            onClick={() => setSelectedRole('recruiter')}
          >
            <div className={styles['role-icon']}>💼</div>
            <h3>Recruiter</h3>
            <p>Posting jobs and finding talented students</p>
          </div>
        </div>

        {error && <div className="error-message" style={{ marginBottom: '20px' }}>{error}</div>}

        <button
          onClick={handleRoleSubmit}
          className="btn btn-primary"
          style={{ width: '100%' }}
          disabled={!selectedRole || loading}
        >
          {loading ? 'Setting up your account...' : 'Continue'}
        </button>
      </div>
    </div>
  );
}

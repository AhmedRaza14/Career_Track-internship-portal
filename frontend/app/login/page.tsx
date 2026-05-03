'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { GoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import styles from '../../styles/auth.module.css';

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Backend expects form-data with 'username' field (not 'email')
      const formDataToSend = new URLSearchParams();
      formDataToSend.append('username', formData.email);
      formDataToSend.append('password', formData.password);

      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/login`, formDataToSend, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token, user_id, role } = response.data;

      localStorage.setItem('token', access_token);
      localStorage.setItem('user_id', user_id);
      localStorage.setItem('role', role);

      router.push('/dashboard');
    } catch (err: any) {
      // Handle error properly - detail might be a string or object
      const errorDetail = err.response?.data?.detail;
      if (typeof errorDetail === 'string') {
        setError(errorDetail);
      } else if (Array.isArray(errorDetail)) {
        setError(errorDetail.map((e: any) => e.msg).join(', '));
      } else {
        setError('Login failed. Please check your credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSuccess = async (credentialResponse: any) => {
    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/auth/google`, {
        token: credentialResponse.credential,
      });

      const { access_token, needs_role_selection, role, user_id } = response.data;

      if (needs_role_selection) {
        localStorage.setItem('temp_token', access_token);
        localStorage.setItem('user_id', user_id);
        router.push('/select-role');
      } else {
        localStorage.setItem('token', access_token);
        localStorage.setItem('role', role);
        localStorage.setItem('user_id', user_id);
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Google authentication failed.');
    }
  };

  return (
    <div className={styles['auth-container']}>
      <div className={styles['auth-card']}>
        <Link href="/" className={styles['back-link']}>
          ← Back to Home
        </Link>

        <div className={styles['auth-header']}>
          <h1>Welcome Back</h1>
          <p>Login to your CareerTrack account</p>
        </div>

        <div className={styles['google-button-wrapper']}>
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => setError('Google login failed')}
            useOneTap
          />
        </div>

        <div className={styles['google-divider']}>
          <span>or login with email</span>
        </div>

        <form onSubmit={handleSubmit} className={styles['auth-form']}>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              name="email"
              className="form-input"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className={styles['auth-footer']}>
          Don't have an account? <Link href="/register">Register here</Link>
        </div>
      </div>
    </div>
  );
}

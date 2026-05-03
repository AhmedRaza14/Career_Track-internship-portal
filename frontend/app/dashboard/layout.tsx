'use client';

import { usePathname, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import axios from 'axios';
import styles from '../../styles/dashboard.module.css';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const [role, setRole] = useState('');
  const [unreadCount, setUnreadCount] = useState(0);
  const [userName, setUserName] = useState('');
  const [profilePicture, setProfilePicture] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('role');
    const userId = localStorage.getItem('user_id');

    if (!token) {
      router.push('/login');
      return;
    }

    if (userRole) {
      setRole(userRole);
    }

    // Fetch user profile data
    if (userId) {
      fetchUserProfile(token, userId);
    }

    // Fetch unread message count
    fetchUnreadCount(token);

    // Refresh unread count every 30 seconds
    const interval = setInterval(() => {
      fetchUnreadCount(token);
    }, 30000);

    return () => clearInterval(interval);
  }, [router]);

  const fetchUserProfile = async (token: string, userId: string) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/profile/${userId}`, { headers });
      setUserName(response.data.user.full_name);
      setProfilePicture(response.data.user.profile_picture || '');
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }
  };

  const fetchUnreadCount = async (token: string) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/messages/conversations`, { headers });
      const conversations = response.data;

      // Calculate total unread count
      const total = conversations.reduce((sum: number, conv: any) => sum + (conv.unread_count || 0), 0);
      setUnreadCount(total);
    } catch (error) {
      console.error('Error fetching unread count:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('role');
    router.push('/');
  };

  const getInitials = (name: string) => {
    if (!name) return '?';
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/profile', label: 'My Profile', icon: '👤' },
    { path: '/jobs', label: 'Jobs', icon: '💼' },
    { path: '/collaboration', label: 'Collaboration', icon: '🤝' },
    { path: '/messages', label: 'Messages', icon: '💬' },
  ];

  return (
    <div className={styles['dashboard-layout']}>
      <aside className={styles.sidebar}>
        <div className={styles['sidebar-header']}>
          <div className={styles['sidebar-logo']}>CareerTrack</div>
          {role && (
            <div style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '8px' }}>
              {role.charAt(0).toUpperCase() + role.slice(1)}
            </div>
          )}
        </div>

        {/* Profile Picture Section */}
        {pathname !== '/profile' && (
          <div className={styles['sidebar-profile']}>
            <div className={styles['sidebar-avatar']}>
              {profilePicture ? (
                <img src={profilePicture} alt={userName} />
              ) : (
                <div className={styles['avatar-initials']}>{getInitials(userName)}</div>
              )}
            </div>
            {userName && (
              <div className={styles['sidebar-username']}>{userName}</div>
            )}
          </div>
        )}

        <nav className={styles['sidebar-nav']}>
          {navItems.map((item) => (
            <Link key={item.path} href={item.path}>
              <div className={`${styles['nav-item']} ${pathname === item.path ? styles.active : ''}`}>
                <span className={styles['nav-icon']}>{item.icon}</span>
                {item.label}
                {item.path === '/messages' && unreadCount > 0 && (
                  <span className={styles['notification-badge']}>
                    {unreadCount}
                  </span>
                )}
              </div>
            </Link>
          ))}
        </nav>

        <div className={styles['sidebar-footer']}>
          <button
            onClick={handleLogout}
            className="btn btn-danger"
            style={{ width: '100%' }}
          >
            Logout
          </button>
        </div>
      </aside>

      <main className={styles['main-content']}>
        {children}
      </main>
    </div>
  );
}

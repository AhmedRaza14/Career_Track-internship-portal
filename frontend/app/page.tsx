'use client';

import Link from 'next/link';
import styles from '../styles/landing.module.css';

export default function LandingPage() {
  return (
    <div className={styles.landing}>
      <nav className={styles.navbar}>
        <div className="container">
          <div className={styles['navbar-content']}>
            <div className={styles.logo}>CareerTrack</div>
            <div className={styles['nav-buttons']}>
              <Link href="/login">
                <button className="btn btn-outline">Login</button>
              </Link>
              <Link href="/register">
                <button className="btn btn-primary">Register</button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <section className={styles.hero}>
        <div className={styles['hero-content']}>
          <h1>Build Your Professional Profile</h1>
          <p>
            Connect with recruiters, discover internships and jobs, find collaborators,
            and take your career to the next level.
          </p>
          <div className={styles['hero-buttons']}>
            <Link href="/register">
              <button className="btn btn-primary" style={{ fontSize: '18px', padding: '12px 30px' }}>
                Get Started
              </button>
            </Link>
            <Link href="/login">
              <button className="btn btn-outline" style={{ fontSize: '18px', padding: '12px 30px' }}>
                Sign In
              </button>
            </Link>
          </div>
        </div>
      </section>

      <section className={styles.features}>
        <div className="container">
          <h2>Why Choose CareerTrack?</h2>
          <div className={styles['features-grid']}>
            <div className={styles['feature-card']}>
              <div className={styles['feature-icon']}>👤</div>
              <h3>Professional Profile</h3>
              <p>Create a comprehensive profile showcasing your skills, projects, and certifications</p>
            </div>
            <div className={styles['feature-card']}>
              <div className={styles['feature-icon']}>💼</div>
              <h3>Job Opportunities</h3>
              <p>Browse and apply for internships and jobs from top companies</p>
            </div>
            <div className={styles['feature-card']}>
              <div className={styles['feature-icon']}>🤝</div>
              <h3>Collaboration</h3>
              <p>Find students to collaborate on projects and build together</p>
            </div>
            <div className={styles['feature-card']}>
              <div className={styles['feature-icon']}>💬</div>
              <h3>Direct Messaging</h3>
              <p>Connect directly with recruiters and other students</p>
            </div>
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <p>&copy; 2026 CareerTrack. All rights reserved.</p>
      </footer>
    </div>
  );
}

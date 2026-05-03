# Google OAuth Setup Guide for CareerTrack

## Overview

CareerTrack now supports two authentication methods:
1. **Email/Password** - Traditional registration
2. **Google OAuth** - "Continue with Google" button

## 🔧 Backend Setup

### Step 1: Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)

2. **Create a New Project** (or select existing)
   - Click "Select a project" → "New Project"
   - Name: `CareerTrack`
   - Click "Create"

3. **Enable Google+ API**
   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - If prompted, configure OAuth consent screen first:
     - User Type: External
     - App name: CareerTrack
     - User support email: your email
     - Developer contact: your email
     - Click "Save and Continue"
     - Scopes: Add `email`, `profile`, `openid`
     - Test users: Add your email
     - Click "Save and Continue"

5. **Configure OAuth Client**
   - Application type: **Web application**
   - Name: `CareerTrack Web Client`
   - Authorized JavaScript origins:
     ```
     http://localhost:3000
     http://localhost:5173
     ```
   - Authorized redirect URIs:
     ```
     http://localhost:3000/auth/callback
     http://localhost:5173/auth/callback
     ```
   - Click "Create"

6. **Copy Your Client ID**
   - You'll see a popup with Client ID and Client Secret
   - Copy the **Client ID** (looks like: `123456789-abc123.apps.googleusercontent.com`)
   - You only need the Client ID for this implementation

### Step 2: Update Backend .env File

Add your Google Client ID to `.env`:

```env
GOOGLE_CLIENT_ID=your-actual-client-id.apps.googleusercontent.com
```

### Step 3: Restart Backend Server

The database schema has changed, so you need to restart:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

**Note:** The database will automatically update with new columns.

---

## 🎨 Frontend Integration

### Step 1: Install Google OAuth Library

```bash
npm install @react-oauth/google
# or
yarn add @react-oauth/google
```

### Step 2: Wrap App with GoogleOAuthProvider

```jsx
// main.jsx or App.jsx
import { GoogleOAuthProvider } from '@react-oauth/google';

const GOOGLE_CLIENT_ID = "your-client-id.apps.googleusercontent.com";

function App() {
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      {/* Your app components */}
    </GoogleOAuthProvider>
  );
}
```

### Step 3: Add Google Login Button

```jsx
import { GoogleLogin } from '@react-oauth/google';
import axios from 'axios';

function LoginPage() {
  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      // Send Google token to backend
      const response = await axios.post('http://localhost:8001/auth/google', {
        token: credentialResponse.credential
      });

      const { access_token, needs_role_selection, role, user_id } = response.data;

      if (needs_role_selection) {
        // New user - show role selection screen
        localStorage.setItem('temp_token', access_token);
        localStorage.setItem('user_id', user_id);
        // Navigate to role selection page
        window.location.href = '/select-role';
      } else {
        // Existing user - log them in
        localStorage.setItem('token', access_token);
        localStorage.setItem('role', role);
        localStorage.setItem('user_id', user_id);
        // Navigate to dashboard
        window.location.href = '/dashboard';
      }
    } catch (error) {
      console.error('Google login failed:', error);
      alert(error.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div>
      <h1>Login to CareerTrack</h1>

      {/* Google Login Button */}
      <GoogleLogin
        onSuccess={handleGoogleSuccess}
        onError={() => console.log('Login Failed')}
        useOneTap
      />

      {/* Or traditional email/password form */}
      <form>
        {/* Email/password fields */}
      </form>
    </div>
  );
}
```

### Step 4: Create Role Selection Page

```jsx
import { useState } from 'react';
import axios from 'axios';

function RoleSelectionPage() {
  const [selectedRole, setSelectedRole] = useState('');

  const handleRoleSubmit = async () => {
    try {
      const tempToken = localStorage.getItem('temp_token');

      const response = await axios.post(
        'http://localhost:8001/auth/google/complete',
        { role: selectedRole },
        {
          headers: {
            'Authorization': `Bearer ${tempToken}`
          }
        }
      );

      const { access_token, role, user_id } = response.data;

      // Save permanent token
      localStorage.setItem('token', access_token);
      localStorage.setItem('role', role);
      localStorage.setItem('user_id', user_id);
      localStorage.removeItem('temp_token');

      // Navigate to dashboard
      window.location.href = '/dashboard';
    } catch (error) {
      console.error('Role selection failed:', error);
      alert('Failed to complete registration');
    }
  };

  return (
    <div>
      <h1>Welcome! Select Your Role</h1>
      <p>Are you a student or a recruiter?</p>

      <button
        onClick={() => setSelectedRole('student')}
        className={selectedRole === 'student' ? 'selected' : ''}
      >
        Student
      </button>

      <button
        onClick={() => setSelectedRole('recruiter')}
        className={selectedRole === 'recruiter' ? 'selected' : ''}
      >
        Recruiter
      </button>

      <button
        onClick={handleRoleSubmit}
        disabled={!selectedRole}
      >
        Continue
      </button>
    </div>
  );
}
```

---

## 🔄 Authentication Flow

### New User Flow (Google OAuth)

```
1. User clicks "Continue with Google"
2. Google login popup appears
3. User authenticates with Google
4. Frontend receives Google ID token
5. Frontend sends token to: POST /auth/google
6. Backend verifies token with Google
7. Backend creates new user (no password, no role yet)
8. Backend returns: needs_role_selection=true
9. Frontend shows role selection screen
10. User selects "Student" or "Recruiter"
11. Frontend sends role to: POST /auth/google/complete
12. Backend updates user with role
13. Backend creates profile
14. Backend returns JWT token
15. User is logged in!
```

### Existing User Flow (Google OAuth)

```
1. User clicks "Continue with Google"
2. Google login popup appears
3. User authenticates with Google
4. Frontend receives Google ID token
5. Frontend sends token to: POST /auth/google
6. Backend verifies token with Google
7. Backend finds existing user by google_id
8. Backend returns: needs_role_selection=false, role, JWT token
9. User is logged in!
```

### Email/Password Flow (Unchanged)

```
1. User enters email + password + role
2. Frontend sends to: POST /register
3. Backend creates user with hashed password
4. Backend returns JWT token
5. User is logged in!
```

---

## 🔒 Security Notes

1. **Google Token Verification**
   - Backend verifies every Google token with Google's servers
   - Invalid tokens are rejected
   - No way to fake authentication

2. **Password Handling**
   - Google users: No password stored (NULL in database)
   - Email users: Password is hashed with bcrypt
   - Users cannot mix auth methods

3. **Role Assignment**
   - Google users must select role on first login
   - Role cannot be changed after selection (add endpoint if needed)
   - Email users select role during registration

---

## 📊 Database Changes

New columns added to `users` table:

```sql
google_id VARCHAR (nullable, unique) - Google user ID
auth_provider VARCHAR - "email" or "google"
profile_picture VARCHAR (nullable) - From Google
hashed_password VARCHAR (nullable) - NULL for Google users
role VARCHAR (nullable) - NULL until Google user selects
```

---

## 🧪 Testing

### Test Google OAuth (Manual)

1. Start backend server
2. Go to http://localhost:8001/docs
3. Test `/auth/google` endpoint:
   - You need a real Google ID token (get from frontend)
   - Or use Google OAuth Playground: https://developers.google.com/oauthplayground

### Test with Frontend

1. Set up frontend with Google OAuth button
2. Click "Continue with Google"
3. Select your Google account
4. Should see role selection screen (new user)
5. Select role
6. Should be logged in

---

## ❓ Troubleshooting

### "Invalid Google token" Error

- Check GOOGLE_CLIENT_ID in .env matches your Google Console
- Make sure token is fresh (expires after 1 hour)
- Verify Google+ API is enabled

### "Email already registered" Error

- User previously registered with email/password
- They must login with email/password
- Cannot switch to Google OAuth

### Role Selection Not Working

- Check temp_token is stored in localStorage
- Verify Authorization header is sent
- Check user doesn't already have a role

---

## 🎯 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/auth/google` | POST | Authenticate with Google token |
| `/auth/google/complete` | POST | Complete registration with role |
| `/register` | POST | Register with email/password |
| `/login` | POST | Login with email/password |

---

## ✅ Implementation Complete!

Your backend now supports:
- ✅ Email/Password authentication
- ✅ Google OAuth authentication
- ✅ Two-step Google registration with role selection
- ✅ Separate auth flows for different providers
- ✅ Profile pictures from Google
- ✅ Secure token verification

Ready to build the frontend! 🚀

# CareerTrack Frontend

React/Next.js frontend for the CareerTrack platform - helping students build professional profiles, discover jobs, and collaborate.

## Features

- **Landing Page** - Platform introduction with registration/login
- **Authentication** - Email/password and Google OAuth support
- **Student Dashboard** - Overview of applications, collaborations, and messages
- **Profile Management** - Skills, projects, certifications, and resume upload
- **Job Board** - Search, filter, and apply for jobs
- **Collaboration** - Find students to work on projects together
- **Messaging** - Direct messaging between users

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Regular CSS (CSS Modules)
- **HTTP Client**: Axios
- **Authentication**: Google OAuth (@react-oauth/google)

## Prerequisites

- Node.js 18+ installed
- Backend server running on http://localhost:8001
- Google OAuth Client ID (optional, for Google login)

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

To get your Google Client ID:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized origins: `http://localhost:3000`
6. Copy the Client ID

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at: http://localhost:3000

## Project Structure

```
frontend/
├── app/                      # Next.js App Router pages
│   ├── page.tsx             # Landing page
│   ├── layout.tsx           # Root layout with Google OAuth provider
│   ├── register/            # Registration page
│   ├── login/               # Login page
│   ├── select-role/         # Role selection for Google OAuth users
│   ├── dashboard/           # Dashboard with sidebar layout
│   ├── profile/             # User profile management
│   ├── jobs/                # Job listings and applications
│   ├── collaboration/       # Collaboration posts
│   └── messages/            # Messaging interface
├── styles/                  # CSS modules
│   ├── globals.css          # Global styles and utilities
│   ├── landing.module.css
│   ├── auth.module.css
│   ├── role.module.css
│   ├── dashboard.module.css
│   ├── profile.module.css
│   ├── jobs.module.css
│   ├── collaboration.module.css
│   └── messages.module.css
├── package.json
├── tsconfig.json
└── next.config.js
```

## Available Pages

### Public Pages
- `/` - Landing page
- `/register` - User registration
- `/login` - User login
- `/select-role` - Role selection (Google OAuth only)

### Protected Pages (Require Authentication)
- `/dashboard` - Main dashboard
- `/profile` - User profile
- `/jobs` - Job listings
- `/collaboration` - Collaboration posts
- `/messages` - Direct messaging

## Authentication Flow

### Email/Password Registration
1. User fills registration form (name, email, password, role)
2. Backend creates account and returns JWT token
3. User is redirected to dashboard

### Google OAuth Registration (New User)
1. User clicks "Continue with Google"
2. Google authentication popup
3. Backend creates account without password
4. User selects role (Student/Recruiter)
5. Backend completes registration
6. User is redirected to dashboard

### Google OAuth Login (Existing User)
1. User clicks "Continue with Google"
2. Google authentication popup
3. Backend verifies and returns JWT token
4. User is redirected to dashboard

## API Integration

All API calls are made to `http://localhost:8001`. The frontend uses Axios for HTTP requests with JWT token authentication.

### Authentication Headers
```javascript
const headers = {
  Authorization: `Bearer ${token}`
};
```

### Local Storage
- `token` - JWT access token
- `user_id` - Current user ID
- `role` - User role (student/recruiter)
- `temp_token` - Temporary token for Google OAuth role selection

## Key Features

### For Students
- Create comprehensive profile with skills, projects, certifications
- Upload resume (PDF)
- Browse and search jobs
- Apply to jobs with resume and cover letter
- Create collaboration posts
- Message recruiters and other students

### For Recruiters
- Post job openings
- View job applicants
- Download applicant resumes
- Message students
- View collaboration posts

## Styling

The project uses regular CSS with CSS Modules for component-specific styles. Global styles and utilities are defined in `styles/globals.css`.

### CSS Variables
```css
--primary-color: #2563eb
--secondary-color: #64748b
--success-color: #10b981
--danger-color: #ef4444
--bg-color: #f8fafc
--text-primary: #0f172a
--text-secondary: #475569
```

### Utility Classes
- `.btn`, `.btn-primary`, `.btn-outline`, `.btn-danger`
- `.form-input`, `.form-textarea`, `.form-select`
- `.card`, `.badge`, `.modal`

## Build for Production

```bash
npm run build
npm start
```

## Troubleshooting

### "Failed to fetch" errors
- Ensure backend server is running on http://localhost:8001
- Check CORS is enabled in backend

### Google OAuth not working
- Verify GOOGLE_CLIENT_ID in .env.local
- Check authorized origins in Google Cloud Console
- Ensure backend has matching GOOGLE_CLIENT_ID

### Authentication issues
- Clear localStorage and try logging in again
- Check JWT token is being sent in Authorization header
- Verify backend SECRET_KEY matches

## Development Notes

- All pages use TypeScript for type safety
- Client components are marked with 'use client' directive
- Protected routes check for token in localStorage
- Modal overlays use portal-like behavior with z-index
- Messages auto-scroll to bottom on new message

## License

MIT

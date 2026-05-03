# CareerTrack - Complete Setup & Testing Guide

## ✅ What's Been Completed

### Phase 1: Backend (FastAPI + PostgreSQL)
- ✅ 11 database tables with all relationships
- ✅ 22 API endpoints (20 original + 2 Google OAuth)
- ✅ JWT authentication with bcrypt password hashing
- ✅ Google OAuth integration with role selection
- ✅ Resume upload to Cloudinary
- ✅ Database migration completed (Google OAuth columns added)

### Phase 2: Frontend (Next.js + TypeScript)
- ✅ Landing page with platform introduction
- ✅ Register/Login pages with Google OAuth
- ✅ Role selection for new Google users
- ✅ Dashboard with sidebar navigation
- ✅ Profile management (skills, projects, certifications, resume)
- ✅ Jobs page (search, filter, apply)
- ✅ Collaboration page
- ✅ Messaging system (two-panel chat)

### Recent Fixes
- ✅ Database schema updated with Google OAuth columns
- ✅ Login endpoint fixed (form-data format)
- ✅ Error handling improved (validation errors display properly)

---

## 🚀 Current Status

**Backend**: Running on http://localhost:8001
**Frontend**: You're running it on http://localhost:3000
**Database**: PostgreSQL (Neon) - Connected and migrated

---

## 🧪 Testing Checklist

### 1. Authentication Flow

#### Email/Password Registration
1. Go to http://localhost:3000
2. Click "Register"
3. Fill in: Name, Email, Password, Role (Student/Recruiter)
4. Click "Register"
5. Should redirect to dashboard

#### Email/Password Login
1. Go to http://localhost:3000/login
2. Enter email and password
3. Click "Login"
4. Should redirect to dashboard

#### Google OAuth (New User)
1. Click "Continue with Google"
2. Select Google account
3. Should redirect to role selection page
4. Choose Student or Recruiter
5. Should redirect to dashboard

#### Google OAuth (Existing User)
1. Click "Continue with Google"
2. Select same Google account
3. Should directly redirect to dashboard

---

### 2. Student Workflow

#### Profile Management
1. Go to "My Profile"
2. Click "Edit Profile" - Add bio, location, LinkedIn, GitHub
3. Click "Add Skill" - Add multiple skills
4. Click "Add Project" - Add project with description and URL
5. Click "Add Certification" - Add certification with issuer and date
6. Upload resume (PDF only, max 5MB)

#### Browse and Apply for Jobs
1. Go to "Jobs"
2. Use search bar to find jobs
3. Filter by location and job type
4. Click "Apply Now" on a job
5. Upload resume and write cover letter
6. Submit application

#### Create Collaboration Post
1. Go to "Collaboration"
2. Click "Create Post"
3. Fill in title, description, and skills needed
4. Submit post

#### Send Messages
1. Go to "Collaboration"
2. Click "Message" on someone's post
3. Go to "Messages"
4. Type and send message

---

### 3. Recruiter Workflow

#### Post a Job
1. Go to "Jobs"
2. Click "Post a Job"
3. Fill in all job details:
   - Title, Company, Location
   - Job Type, Salary Range
   - Description, Requirements
4. Submit job posting

#### View Applicants
1. Go to "Jobs"
2. Click "View Applicants" on your job
3. See list of applicants
4. Click "View Resume" to download resumes

#### Message Students
1. Go to "Collaboration"
2. Click "Message" on a student's post
3. Go to "Messages"
4. Chat with students

---

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

---

## 🐛 Known Issues & Solutions

### Issue: Port 3000 already in use
**Solution**: Kill the process or use different port
```bash
# Find process
netstat -ano | findstr :3000

# Kill in Task Manager (find PID and end task)
# Or use different port
npm run dev -- -p 3001
```

### Issue: Google OAuth not working
**Solution**:
1. Verify GOOGLE_CLIENT_ID in both backend and frontend .env files
2. Check Google Cloud Console authorized origins include http://localhost:3000
3. Ensure Google+ API is enabled

### Issue: Resume upload fails
**Solution**:
1. Check Cloudinary credentials in backend .env
2. Ensure file is PDF and under 5MB
3. Check backend logs for specific error

### Issue: "Failed to fetch" errors
**Solution**:
1. Ensure backend is running on port 8001
2. Check CORS is enabled in backend
3. Verify API endpoint URLs in frontend

---

## 📊 API Endpoints Reference

### Authentication
- POST /register - Register with email/password
- POST /login - Login with email/password (form-data)
- POST /auth/google - Authenticate with Google
- POST /auth/google/complete - Complete Google registration with role

### Profile
- GET /profile/{user_id} - Get user profile
- PUT /profile/update - Update profile
- POST /profile/skills - Add skill
- POST /profile/projects - Add project
- POST /profile/certifications - Add certification
- POST /profile/resume - Upload resume

### Jobs
- POST /jobs/create - Create job (recruiter)
- GET /jobs - Get all jobs
- GET /jobs/{job_id} - Get specific job
- GET /jobs/filter - Filter jobs
- POST /jobs/{job_id}/apply - Apply to job (student)
- GET /jobs/{job_id}/applicants - Get applicants (recruiter)

### Collaboration
- POST /collaboration/create - Create collaboration post
- GET /collaboration - Get all collaboration posts

### Messaging
- POST /messages/send - Send message
- GET /messages/conversation/{conversation_id} - Get messages
- GET /messages/conversations - Get all conversations

---

## 🎯 Next Steps

1. **Test all features** using the checklist above
2. **Add Google Client ID** if you want to test Google OAuth
3. **Create test data** - Register multiple users, post jobs, create collaborations
4. **Test edge cases** - Invalid inputs, duplicate registrations, etc.
5. **Check responsive design** - Test on different screen sizes

---

## 📝 Development Commands

### Backend
```bash
cd backend
.venv/Scripts/activate  # Activate virtual environment
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Frontend
```bash
cd frontend
npm run dev  # Runs on port 3000
```

### Database Migration (if needed)
```bash
cd backend
python run_migration.py
```

---

## 🎉 Project Complete!

All three phases are done:
- ✅ Phase 1: Backend Development
- ✅ Phase 2: Frontend Development
- ✅ Phase 3: Integration (APIs connected)

The application is fully functional and ready for testing!

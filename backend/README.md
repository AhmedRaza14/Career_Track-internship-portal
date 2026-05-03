# CareerTrack Backend API

FastAPI-based backend for CareerTrack - A platform connecting students with internships, jobs, and collaboration opportunities.

## 🚀 Quick Start

### 1. Setup Virtual Environment and Install Dependencies

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh start.sh
./setup.sh
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` file:
```env
DATABASE_URL=postgresql://user:password@host:5432/careertrack
SECRET_KEY=your-secret-key-here
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

**Get Free Database:** [Neon.tech](https://neon.tech) - Free PostgreSQL database
**Get Free Storage:** [Cloudinary](https://cloudinary.com) - Free cloud storage for resumes

### 3. Start the Server

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
./start.sh
```

The server will run on **http://localhost:8001**

### 4. Access API Documentation

- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

## 📋 Phase 1 Requirements - ALL COMPLETED ✅

### Database Tables (11/11)
✅ Users - Authentication and user management
✅ Profiles - User profile information
✅ Skills - Master skill list
✅ StudentSkills - Many-to-many user skills
✅ Projects - Student project portfolio
✅ Certifications - Professional certifications
✅ Jobs - Job postings by recruiters
✅ Applications - Job applications with resumes
✅ CollaborationPosts - Collaboration opportunities
✅ Conversations - Message conversations
✅ Messages - Individual messages

### API Endpoints (18/18)

**Authentication (3)**
- `POST /register` - Register new user (student/recruiter)
- `POST /login` - Login and get JWT token
- `POST /logout` - Logout user

**Profile Management (5)**
- `GET /profile/{user_id}` - Get user profile
- `PUT /profile/update` - Update own profile
- `POST /profile/skills` - Add skill to profile
- `POST /profile/projects` - Add project to profile
- `POST /profile/certifications` - Add certification

**Jobs (4)**
- `POST /jobs/create` - Create job (recruiters only)
- `GET /jobs` - Get all active jobs
- `GET /jobs/{job_id}` - Get specific job
- `GET /jobs/filter` - Filter jobs by type/location/skills

**Applications (2)**
- `POST /jobs/{job_id}/apply` - Apply with resume upload
- `GET /jobs/{job_id}/applicants` - View applicants (recruiters only)

**Collaboration (2)**
- `POST /collaboration/create` - Create collaboration post
- `GET /collaboration` - Get all collaboration posts

**Messaging (3)**
- `POST /messages/send` - Send message to user
- `GET /messages/conversation/{id}` - Get conversation messages
- `GET /messages/conversations` - Get all user conversations

### Core Features
✅ JWT Authentication with role-based access
✅ Password hashing with bcrypt
✅ Resume upload to Cloudinary (PDF only, 5MB max)
✅ Duplicate application prevention
✅ Auto-generated Swagger documentation
✅ CORS enabled for frontend integration

## 🧪 Testing the API

### Using Swagger UI (Recommended)

1. Go to http://localhost:8001/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

### Authentication Flow

1. **Register a Student:**
```json
POST /register
{
  "email": "student@test.com",
  "password": "password123",
  "role": "student",
  "full_name": "John Doe"
}
```

2. **Register a Recruiter:**
```json
POST /register
{
  "email": "recruiter@company.com",
  "password": "password123",
  "role": "recruiter",
  "full_name": "Jane Smith"
}
```

3. **Login:**
```
POST /login
username: student@test.com
password: password123
```

4. **Use Token:**
- Copy the `access_token` from response
- Click "Authorize" button in Swagger
- Enter: `Bearer <your_token>`
- Now you can access protected endpoints

## 🏗️ Project Structure

```
backend/
├── .venv/                    # Virtual environment (created by setup)
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI app with all endpoints
│   ├── models.py            # SQLModel database models (11 tables)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── database.py          # PostgreSQL connection
│   ├── auth.py              # JWT authentication
│   └── file_upload.py       # Cloudinary resume upload
├── .env.example             # Environment variables template
├── .env                     # Your environment variables (create this)
├── .gitignore              # Git ignore patterns
├── requirements.txt         # Python dependencies
├── setup.bat / setup.sh     # Setup scripts
├── start.bat / start.sh     # Startup scripts
└── README.md               # This file
```

## 🔒 Security Features

- JWT token authentication
- Password hashing with bcrypt
- Role-based access control (Student/Recruiter)
- Protected endpoints
- File type validation (PDF only)
- File size limits (5MB max)
- SQL injection prevention (SQLModel ORM)
- Duplicate application prevention

## 📦 Tech Stack

- **Framework:** FastAPI 0.115.0
- **Database:** PostgreSQL (via Neon)
- **ORM:** SQLModel 0.0.22
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Bcrypt (passlib)
- **File Storage:** Cloudinary
- **Server:** Uvicorn

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## 📝 API Usage Examples

### Create a Job (Recruiter)
```bash
curl -X POST "http://localhost:8001/jobs/create" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer Intern",
    "company": "Tech Corp",
    "description": "Looking for talented interns",
    "job_type": "internship",
    "location": "Remote",
    "required_skills": "Python, FastAPI"
  }'
```

### Apply for Job (Student)
```bash
curl -X POST "http://localhost:8001/jobs/1/apply" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "resume=@resume.pdf" \
  -F "cover_letter=I am interested in this position"
```

### Send Message
```bash
curl -X POST "http://localhost:8001/messages/send" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_id": 2,
    "content": "Hello, I am interested in your collaboration post"
  }'
```

## 🐛 Troubleshooting

### Virtual Environment Issues
```bash
# Windows: If activation fails
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux/Mac: If permission denied
chmod +x setup.sh start.sh
```

### Database Connection Issues
- Verify DATABASE_URL in .env file
- Check if PostgreSQL is running
- Test connection string

### Cloudinary Upload Issues
- Verify Cloudinary credentials in .env
- Check file is PDF format
- Ensure file size is under 5MB

## 🎯 Next Steps

### Phase 2 - Frontend Development
- Build React/Next.js frontend
- Create pages (Landing, Dashboard, Profile, Jobs, etc.)
- Implement forms and UI components

### Phase 3 - Integration
- Connect frontend to backend APIs
- Implement JWT token storage
- Add protected routes
- End-to-end testing

## 📞 Support

- **API Docs:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

---

**Phase 1 Status: ✅ COMPLETE**

All backend requirements successfully implemented and ready for testing!

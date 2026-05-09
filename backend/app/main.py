from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from typing import List, Optional
from datetime import timedelta
from pathlib import Path

from app.database import create_db_and_tables, get_session
from app.models import (
    User, Profile, Skill, StudentSkill, Project, Certification,
    Job, Application, CollaborationPost, Conversation, Message, UserRole, JobType
)
from app.schemas import (
    UserRegister, UserLogin, Token, UserResponse, ProfileUpdate, ProfileResponse,
    SkillCreate, SkillResponse, ProfileSkillResponse, ProjectCreate, ProjectResponse,
    CertificationCreate, CertificationResponse, JobCreate, JobResponse,
    ApplicationCreate, ApplicationResponse, ApplicantResponse,
    CollaborationCreate, CollaborationResponse, MessageSend, MessageResponse,
    ConversationResponse, GoogleAuthRequest, GoogleAuthResponse, RoleSelectionRequest,
    CompleteProfileResponse, UserBasicInfo
)
from app.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.file_upload import upload_resume, upload_profile_picture
from app.google_auth import verify_google_token

app = FastAPI(
    title="CareerTrack API",
    description="Backend API for CareerTrack - A platform connecting students with internships, jobs, and collaboration opportunities",
    version="1.0.0"
)

# Get absolute path to uploads directory
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for resume uploads
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {
        "message": "Welcome to CareerTrack API",
        "docs": "/docs",
        "version": "1.0.0"
    }

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, session: Session = Depends(get_session)):
    """Register a new user (student or recruiter) with email/password"""
    # Check if user already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        auth_provider="email",  # Email/password authentication
        role=user_data.role,
        full_name=user_data.full_name
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Create profile for the user
    new_profile = Profile(user_id=new_user.id)
    session.add(new_profile)
    session.commit()

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": new_user.id,
        "role": new_user.role
    }

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Login user with email/password and return JWT token"""
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is Google OAuth user
    if user.auth_provider == "google":
        raise HTTPException(
            status_code=400,
            detail="This account uses Google authentication. Please login with Google."
        )

    # Verify password for email/password users
    if not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role
    }

@app.post("/logout")
def logout(current_user: User = Depends(get_current_active_user)):
    """Logout user (client should delete token)"""
    return {"message": "Successfully logged out"}

# ==================== GOOGLE OAUTH ENDPOINTS ====================

@app.post("/auth/google", response_model=GoogleAuthResponse)
async def google_auth(auth_data: GoogleAuthRequest, session: Session = Depends(get_session)):
    """
    Authenticate with Google OAuth

    Flow:
    1. Frontend gets Google ID token
    2. Send token to this endpoint
    3. If new user: returns needs_role_selection=True
    4. If existing user: returns JWT token and logs in
    """
    # Verify Google token and get user info
    google_user = await verify_google_token(auth_data.token)

    # Check if user exists
    statement = select(User).where(User.google_id == google_user["google_id"])
    existing_user = session.exec(statement).first()

    if existing_user:
        # Existing user - log them in
        if not existing_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": existing_user.email}, expires_delta=access_token_expires
        )

        return GoogleAuthResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=existing_user.id,
            needs_role_selection=False,
            role=existing_user.role
        )
    else:
        # New user - check if email already exists with different auth provider
        statement = select(User).where(User.email == google_user["email"])
        email_user = session.exec(statement).first()
        if email_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered with password authentication. Please login with email/password."
            )

        # Create new user without role (will be set in complete endpoint)
        new_user = User(
            email=google_user["email"],
            google_id=google_user["google_id"],
            auth_provider="google",
            full_name=google_user["name"],
            profile_picture=google_user["picture"],
            hashed_password=None,  # No password for Google users
            role=None  # Will be set in complete endpoint
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Create access token (temporary, until role is selected)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": new_user.email}, expires_delta=access_token_expires
        )

        return GoogleAuthResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=new_user.id,
            needs_role_selection=True,
            role=None
        )

@app.post("/auth/google/complete", response_model=Token)
def complete_google_registration(
    role_data: RoleSelectionRequest,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Complete Google OAuth registration by selecting role

    Called after /auth/google when needs_role_selection=True
    """
    # Check if user already has a role
    if current_user.role is not None:
        raise HTTPException(status_code=400, detail="User already has a role assigned")

    # Check if user is Google OAuth user
    if current_user.auth_provider != "google":
        raise HTTPException(status_code=400, detail="This endpoint is only for Google OAuth users")

    # Update user role
    current_user.role = role_data.role
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    # Create profile for the user
    new_profile = Profile(user_id=current_user.id)
    session.add(new_profile)
    session.commit()

    # Create new access token with role
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": current_user.id,
        "role": current_user.role
    }

# ==================== PROFILE ENDPOINTS ====================

@app.get("/profile/{user_id}", response_model=CompleteProfileResponse)
def get_profile(user_id: int, session: Session = Depends(get_session)):
    """Get complete user profile with all related data"""
    # Get user
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get profile
    statement = select(Profile).where(Profile.user_id == user_id)
    profile = session.exec(statement).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Get skills (join student_skills with skills)
    statement = select(StudentSkill).where(StudentSkill.profile_id == profile.id)
    student_skills = session.exec(statement).all()

    skills = []
    for ss in student_skills:
        skill = session.get(Skill, ss.skill_id)
        if skill:
            skills.append({
                "id": skill.id,
                "skill_name": skill.name,  # Frontend expects skill_name
                "proficiency_level": ss.proficiency_level
            })

    # Get projects
    statement = select(Project).where(Project.profile_id == profile.id)
    projects = session.exec(statement).all()

    # Get certifications
    statement = select(Certification).where(Certification.profile_id == profile.id)
    certifications = session.exec(statement).all()

    # Build response
    return {
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "profile_picture": user.profile_picture
        },
        "profile": profile,
        "skills": skills,
        "projects": projects,
        "certifications": certifications
    }

@app.put("/profile/update", response_model=ProfileResponse)
def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Update current user's profile"""
    statement = select(Profile).where(Profile.user_id == current_user.id)
    profile = session.exec(statement).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Update profile fields
    for key, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile

@app.post("/profile/skills", response_model=SkillResponse)
def add_skill(
    skill_data: SkillCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Add skill to current user's profile"""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Only students can add skills")

    # Get user's profile
    statement = select(Profile).where(Profile.user_id == current_user.id)
    profile = session.exec(statement).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Check if skill exists, if not create it
    statement = select(Skill).where(Skill.name == skill_data.skill_name)
    skill = session.exec(statement).first()
    if not skill:
        skill = Skill(name=skill_data.skill_name)
        session.add(skill)
        session.commit()
        session.refresh(skill)

    # Check if student already has this skill
    statement = select(StudentSkill).where(
        StudentSkill.profile_id == profile.id,
        StudentSkill.skill_id == skill.id
    )
    existing = session.exec(statement).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already added")

    # Add skill to student profile
    student_skill = StudentSkill(
        profile_id=profile.id,
        skill_id=skill.id,
        proficiency_level=skill_data.proficiency_level
    )
    session.add(student_skill)
    session.commit()
    session.refresh(student_skill)

    return {
        "id": skill.id,
        "name": skill.name,
        "proficiency_level": student_skill.proficiency_level
    }

@app.post("/profile/projects", response_model=ProjectResponse)
def add_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Add project to current user's profile"""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Only students can add projects")

    # Get user's profile
    statement = select(Profile).where(Profile.user_id == current_user.id)
    profile = session.exec(statement).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Create project
    project = Project(
        profile_id=profile.id,
        **project_data.model_dump()
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

@app.post("/profile/certifications", response_model=CertificationResponse)
def add_certification(
    cert_data: CertificationCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Add certification to current user's profile"""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Only students can add certifications")

    # Get user's profile
    statement = select(Profile).where(Profile.user_id == current_user.id)
    profile = session.exec(statement).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Create certification
    cert_dict = cert_data.model_dump()
    # Map 'issuer' from frontend to 'issuing_organization' in database
    if 'issuer' in cert_dict:
        cert_dict['issuing_organization'] = cert_dict.pop('issuer')

    certification = Certification(
        profile_id=profile.id,
        **cert_dict
    )
    session.add(certification)
    session.commit()
    session.refresh(certification)
    return certification

@app.post("/profile/resume")
async def upload_profile_resume(
    resume: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Upload resume to user profile"""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Only students can upload resumes")

    # Get user's profile
    statement = select(Profile).where(Profile.user_id == current_user.id)
    profile = session.exec(statement).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Upload resume to Cloudinary
    resume_url = await upload_resume(resume)

    # Update profile with resume URL
    profile.resume_url = resume_url
    session.add(profile)
    session.commit()
    session.refresh(profile)

    return {"message": "Resume uploaded successfully", "resume_url": resume_url}

@app.post("/profile/picture")
async def upload_user_profile_picture(
    picture: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Upload profile picture for user"""
    # Upload picture to local storage
    picture_url = await upload_profile_picture(picture)

    # Update user's profile_picture field
    current_user.profile_picture = picture_url
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return {"message": "Profile picture uploaded successfully", "profile_picture": picture_url}

# ==================== JOB ENDPOINTS ====================

@app.post("/jobs/create", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Create a new job posting (recruiters only)"""
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=403, detail="Only recruiters can create jobs")
    
    # Validate job_type - convert string to JobType enum
    try:
        job_type_enum = JobType(job_data.job_type.replace('-', '_'))
    except ValueError:
        valid_types = [t.value for t in JobType]
        raise HTTPException(status_code=400, detail=f"Invalid job type. Must be one of: {valid_types}")
    
    # Create job with all fields including experience_level and deadline
    job = Job(
        recruiter_id=current_user.id,
        title=job_data.title,
        company=job_data.company,
        description=job_data.description,
        job_type=job_type_enum,
        location=job_data.location,
        salary_range=job_data.salary_range,
        required_skills=job_data.required_skills,
        experience_level=job_data.experience_level,  # ADDED
        deadline=job_data.deadline,  # ADDED
        is_active=True
    )
    session.add(job)
    session.commit()
    session.refresh(job)
    
    # Return response with all fields
    return {
        "id": job.id,
        "recruiter_id": job.recruiter_id,
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "job_type": job.job_type.value,
        "location": job.location,
        "salary_range": job.salary_range,
        "required_skills": job.required_skills,
        "experience_level": job.experience_level,
        "deadline": job.deadline,
        "is_active": job.is_active,
        "created_at": job.created_at
    }
    
@app.get("/jobs", response_model=List[JobResponse])
def get_jobs(session: Session = Depends(get_session)):
    """Get all active jobs"""
    statement = select(Job).where(Job.is_active == True)
    jobs = session.exec(statement).all()
    return jobs

@app.get("/jobs/filter", response_model=List[JobResponse])
def filter_jobs(
    job_type: Optional[JobType] = None,
    location: Optional[str] = None,
    skills: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """Filter jobs by type, location, or skills"""
    statement = select(Job).where(Job.is_active == True)

    if job_type:
        statement = statement.where(Job.job_type == job_type)
    if location:
        statement = statement.where(Job.location.contains(location))
    if skills:
        statement = statement.where(Job.required_skills.contains(skills))

    jobs = session.exec(statement).all()
    return jobs

@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, session: Session = Depends(get_session)):
    """Get specific job by ID"""
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# ==================== APPLICATION ENDPOINTS ====================

@app.post("/jobs/{job_id}/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_for_job(
    job_id: int,
    resume: UploadFile = File(...),
    cover_letter: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Apply for a job with resume upload"""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Only students can apply for jobs")

    # Check if job exists
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check for duplicate application
    statement = select(Application).where(
        Application.job_id == job_id,
        Application.student_id == current_user.id
    )
    existing_application = session.exec(statement).first()
    if existing_application:
        raise HTTPException(status_code=400, detail="You have already applied for this job")

    # Upload resume to Cloudinary
    resume_url = await upload_resume(resume)

    # Create application
    application = Application(
        job_id=job_id,
        student_id=current_user.id,
        resume_url=resume_url,
        cover_letter=cover_letter
    )
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

@app.get("/jobs/{job_id}/applicants", response_model=List[ApplicantResponse])
def get_job_applicants(
    job_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get all applicants for a job (recruiters only)"""
    if current_user.role != UserRole.RECRUITER:
        raise HTTPException(status_code=403, detail="Only recruiters can view applicants")

    # Check if job exists and belongs to current recruiter
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only view applicants for your own jobs")

    # Get all applications for this job
    statement = select(Application).where(Application.job_id == job_id)
    applications = session.exec(statement).all()

    # Format response with student details
    applicants = []
    for app in applications:
        student = session.get(User, app.student_id)
        applicants.append({
            "application_id": app.id,
            "student_id": student.id,
            "student_name": student.full_name,
            "student_email": student.email,
            "resume_url": app.resume_url,
            "cover_letter": app.cover_letter,
            "status": app.status,
            "applied_at": app.applied_at
        })

    return applicants

@app.get("/applications/my", response_model=List[ApplicationResponse])
def get_my_applications(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get all applications submitted by current student"""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=403, detail="Only students can view their applications")

    # Get all applications for this student
    statement = select(Application).where(Application.student_id == current_user.id)
    applications = session.exec(statement).all()
    return applications

# ==================== COLLABORATION ENDPOINTS ====================

@app.post("/collaboration/create", response_model=CollaborationResponse, status_code=status.HTTP_201_CREATED)
def create_collaboration(
    collab_data: CollaborationCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Create a new collaboration post"""
    collaboration = CollaborationPost(
        author_id=current_user.id,
        **collab_data.model_dump()
    )
    session.add(collaboration)
    session.commit()
    session.refresh(collaboration)

    return {
        "id": collaboration.id,
        "author_id": collaboration.author_id,
        "author_name": current_user.full_name,
        "title": collaboration.title,
        "description": collaboration.description,
        "required_skills": collaboration.required_skills,
        "project_type": collaboration.project_type,
        "duration": collaboration.duration,
        "is_active": collaboration.is_active,
        "created_at": collaboration.created_at
    }

@app.get("/collaboration", response_model=List[CollaborationResponse])
def get_collaborations(session: Session = Depends(get_session)):
    """Get all active collaboration posts"""
    statement = select(CollaborationPost).where(CollaborationPost.is_active == True)
    collaborations = session.exec(statement).all()

    # Format response with author details
    result = []
    for collab in collaborations:
        author = session.get(User, collab.author_id)
        result.append({
            "id": collab.id,
            "author_id": collab.author_id,
            "author_name": author.full_name,
            "title": collab.title,
            "description": collab.description,
            "required_skills": collab.required_skills,
            "project_type": collab.project_type,
            "duration": collab.duration,
            "is_active": collab.is_active,
            "created_at": collab.created_at
        })

    return result

@app.put("/collaboration/{post_id}", response_model=CollaborationResponse)
def update_collaboration(
    post_id: int,
    collab_data: CollaborationCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Update a collaboration post (author only)"""
    # Get the collaboration post
    collaboration = session.get(CollaborationPost, post_id)
    if not collaboration:
        raise HTTPException(status_code=404, detail="Collaboration post not found")

    # Check if current user is the author
    if collaboration.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own posts")

    # Update the post
    collaboration.title = collab_data.title
    collaboration.description = collab_data.description
    collaboration.required_skills = collab_data.required_skills
    collaboration.project_type = collab_data.project_type
    collaboration.duration = collab_data.duration

    session.add(collaboration)
    session.commit()
    session.refresh(collaboration)

    return {
        "id": collaboration.id,
        "author_id": collaboration.author_id,
        "author_name": current_user.full_name,
        "title": collaboration.title,
        "description": collaboration.description,
        "required_skills": collaboration.required_skills,
        "project_type": collaboration.project_type,
        "duration": collaboration.duration,
        "is_active": collaboration.is_active,
        "created_at": collaboration.created_at
    }

@app.delete("/collaboration/{post_id}")
def delete_collaboration(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Delete a collaboration post (author only)"""
    # Get the collaboration post
    collaboration = session.get(CollaborationPost, post_id)
    if not collaboration:
        raise HTTPException(status_code=404, detail="Collaboration post not found")

    # Check if current user is the author
    if collaboration.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own posts")

    # Delete the post
    session.delete(collaboration)
    session.commit()

    return {"message": "Collaboration post deleted successfully"}


# ==================== MESSAGING ENDPOINTS ====================

@app.post("/messages/send", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    message_data: MessageSend,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Send a message to another user"""
    # Check if receiver exists
    receiver = session.get(User, message_data.receiver_id)
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    # Check if conversation exists
    statement = select(Conversation).where(
        ((Conversation.participant1_id == current_user.id) & (Conversation.participant2_id == message_data.receiver_id)) |
        ((Conversation.participant1_id == message_data.receiver_id) & (Conversation.participant2_id == current_user.id))
    )
    conversation = session.exec(statement).first()

    # Create conversation if it doesn't exist
    if not conversation:
        conversation = Conversation(
            participant1_id=current_user.id,
            participant2_id=message_data.receiver_id
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Create message
    message = Message(
        conversation_id=conversation.id,
        sender_id=current_user.id,
        content=message_data.content
    )
    session.add(message)
    session.commit()
    session.refresh(message)

    # Return message with sender name
    return {
        "id": message.id,
        "conversation_id": message.conversation_id,
        "sender_id": message.sender_id,
        "sender_name": current_user.full_name,
        "content": message.content,
        "is_read": message.is_read,
        "created_at": message.created_at
    }

@app.get("/messages/conversation/{conversation_id}", response_model=List[MessageResponse])
def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get all messages in a conversation"""
    # Check if conversation exists and user is a participant
    conversation = session.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if current_user.id not in [conversation.participant1_id, conversation.participant2_id]:
        raise HTTPException(status_code=403, detail="You are not a participant in this conversation")

    # Get all messages
    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    messages = session.exec(statement).all()

    # Format response with sender names
    result = []
    for msg in messages:
        sender = session.get(User, msg.sender_id)
        result.append({
            "id": msg.id,
            "conversation_id": msg.conversation_id,
            "sender_id": msg.sender_id,
            "sender_name": sender.full_name if sender else "Unknown",
            "content": msg.content,
            "is_read": msg.is_read,
            "created_at": msg.created_at
        })

    return result

@app.put("/messages/conversation/{conversation_id}/mark-read")
def mark_messages_as_read(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Mark all messages in a conversation as read"""
    # Check if conversation exists and user is a participant
    conversation = session.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if current_user.id not in [conversation.participant1_id, conversation.participant2_id]:
        raise HTTPException(status_code=403, detail="You are not a participant in this conversation")

    # Mark all messages from the other user as read
    statement = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.sender_id != current_user.id,
        Message.is_read == False
    )
    messages = session.exec(statement).all()

    for message in messages:
        message.is_read = True
        session.add(message)

    session.commit()

    return {"message": "Messages marked as read", "count": len(messages)}

@app.get("/messages/conversations", response_model=List[ConversationResponse])
def get_user_conversations(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get all conversations for current user"""
    statement = select(Conversation).where(
        (Conversation.participant1_id == current_user.id) |
        (Conversation.participant2_id == current_user.id)
    )
    conversations = session.exec(statement).all()

    # Format response with other user details and last message
    result = []
    for conv in conversations:
        other_user_id = conv.participant2_id if conv.participant1_id == current_user.id else conv.participant1_id
        other_user = session.get(User, other_user_id)

        # Get last message
        statement = select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.desc())
        last_message = session.exec(statement).first()

        # Count unread messages
        statement = select(Message).where(
            Message.conversation_id == conv.id,
            Message.sender_id != current_user.id,
            Message.is_read == False
        )
        unread_count = len(session.exec(statement).all())

        result.append({
            "id": conv.id,
            "participant1_id": conv.participant1_id,
            "participant2_id": conv.participant2_id,
            "other_user_id": other_user_id,  # Add other_user_id for frontend
            "other_user_name": other_user.full_name,
            "last_message": last_message.content if last_message else None,
            "last_message_time": last_message.created_at if last_message else None,
            "unread_count": unread_count,
            "created_at": conv.created_at
        })

    return result

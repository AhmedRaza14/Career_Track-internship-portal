from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, JobType

# Authentication Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleAuthRequest(BaseModel):
    token: str  # Google ID token from frontend

class GoogleAuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    needs_role_selection: bool  # True if new user needs to select role
    role: Optional[UserRole] = None

class RoleSelectionRequest(BaseModel):
    role: UserRole

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    role: UserRole

class UserResponse(BaseModel):
    id: int
    email: str
    role: Optional[UserRole]
    full_name: str
    profile_picture: Optional[str]
    is_active: bool
    created_at: datetime

# Profile Schemas
class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    education: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    bio: Optional[str]
    education: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    linkedin_url: Optional[str]
    github_url: Optional[str]
    portfolio_url: Optional[str]
    resume_url: Optional[str]
    updated_at: datetime

class UserBasicInfo(BaseModel):
    id: int
    full_name: str
    email: str
    profile_picture: Optional[str]

class CompleteProfileResponse(BaseModel):
    user: UserBasicInfo
    profile: ProfileResponse
    skills: List['ProfileSkillResponse']
    projects: List['ProjectResponse']
    certifications: List['CertificationResponse']

# Skill Schemas
class SkillCreate(BaseModel):
    skill_name: str
    proficiency_level: Optional[str] = None

class SkillResponse(BaseModel):
    id: int
    name: str
    proficiency_level: Optional[str]

class ProfileSkillResponse(BaseModel):
    id: int
    skill_name: str
    proficiency_level: Optional[str]

# Project Schemas
class ProjectCreate(BaseModel):
    title: str
    description: str
    technologies: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProjectResponse(BaseModel):
    id: int
    profile_id: int
    title: str
    description: str
    technologies: Optional[str]
    project_url: Optional[str]
    github_url: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime

# Certification Schemas
class CertificationCreate(BaseModel):
    title: str
    issuer: str  # Changed from issuing_organization to match frontend
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None

class CertificationResponse(BaseModel):
    id: int
    profile_id: int
    title: str
    issuing_organization: str
    issue_date: Optional[datetime]
    expiry_date: Optional[datetime]
    credential_id: Optional[str]
    credential_url: Optional[str]
    created_at: datetime

# Job Schemas
class JobCreate(BaseModel):
    title: str
    company: str
    description: str
    job_type: JobType
    location: str
    salary_range: Optional[str] = None
    required_skills: Optional[str] = None
    experience_level: Optional[str] = None
    deadline: Optional[datetime] = None

class JobResponse(BaseModel):
    id: int
    recruiter_id: int
    title: str
    company: str
    description: str
    job_type: JobType
    location: str
    salary_range: Optional[str]
    required_skills: Optional[str]
    experience_level: Optional[str]
    deadline: Optional[datetime]
    is_active: bool
    created_at: datetime

# Application Schemas
class ApplicationCreate(BaseModel):
    cover_letter: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    student_id: int
    resume_url: str
    cover_letter: Optional[str]
    status: str
    applied_at: datetime

class ApplicantResponse(BaseModel):
    application_id: int
    student_id: int
    student_name: str
    student_email: str
    resume_url: str
    cover_letter: Optional[str]
    status: str
    applied_at: datetime

# Collaboration Schemas
class CollaborationCreate(BaseModel):
    title: str
    description: str
    required_skills: Optional[str] = None
    project_type: Optional[str] = None
    duration: Optional[str] = None

class CollaborationResponse(BaseModel):
    id: int
    author_id: int
    author_name: str
    title: str
    description: str
    required_skills: Optional[str]
    project_type: Optional[str]
    duration: Optional[str]
    is_active: bool
    created_at: datetime

# Message Schemas
class MessageSend(BaseModel):
    receiver_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    sender_name: str
    content: str
    is_read: bool
    created_at: datetime

class ConversationResponse(BaseModel):
    id: int
    participant1_id: int
    participant2_id: int
    other_user_id: int  # ID of the other user in conversation
    other_user_name: str
    last_message: Optional[str]
    last_message_time: Optional[datetime]
    unread_count: int
    created_at: datetime

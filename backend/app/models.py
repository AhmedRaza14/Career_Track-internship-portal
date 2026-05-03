from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    RECRUITER = "recruiter"

class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"

class JobType(str, Enum):
    INTERNSHIP = "internship"
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: Optional[str] = None  # Nullable for Google OAuth users
    google_id: Optional[str] = Field(default=None, unique=True, index=True)  # For Google OAuth
    auth_provider: str = Field(default="email")  # Track auth method - stored as string
    role: Optional[UserRole] = None  # Nullable for Google users during registration
    full_name: str
    profile_picture: Optional[str] = None  # From Google OAuth
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    profile: Optional["Profile"] = Relationship(back_populates="user")
    jobs: List["Job"] = Relationship(back_populates="recruiter")
    applications: List["Application"] = Relationship(back_populates="student")
    collaboration_posts: List["CollaborationPost"] = Relationship(back_populates="author")
    sent_messages: List["Message"] = Relationship(back_populates="sender")

class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    bio: Optional[str] = None
    education: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    resume_url: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="profile")
    skills: List["StudentSkill"] = Relationship(back_populates="profile")
    projects: List["Project"] = Relationship(back_populates="profile")
    certifications: List["Certification"] = Relationship(back_populates="profile")

class Skill(SQLModel, table=True):
    __tablename__ = "skills"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    category: Optional[str] = None

    # Relationships
    student_skills: List["StudentSkill"] = Relationship(back_populates="skill")

class StudentSkill(SQLModel, table=True):
    __tablename__ = "student_skills"

    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profiles.id")
    skill_id: int = Field(foreign_key="skills.id")
    proficiency_level: Optional[str] = None  # beginner, intermediate, advanced, expert

    # Relationships
    profile: Optional[Profile] = Relationship(back_populates="skills")
    skill: Optional[Skill] = Relationship(back_populates="student_skills")

class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profiles.id")
    title: str
    description: str
    technologies: Optional[str] = None
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    profile: Optional[Profile] = Relationship(back_populates="projects")

class Certification(SQLModel, table=True):
    __tablename__ = "certifications"

    id: Optional[int] = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profiles.id")
    title: str
    issuing_organization: str
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    profile: Optional[Profile] = Relationship(back_populates="certifications")

class Job(SQLModel, table=True):
    __tablename__ = "jobs"

    id: Optional[int] = Field(default=None, primary_key=True)
    recruiter_id: int = Field(foreign_key="users.id")
    title: str
    company: str
    description: str
    job_type: JobType
    location: str
    salary_range: Optional[str] = None
    required_skills: Optional[str] = None
    experience_level: Optional[str] = None
    deadline: Optional[datetime] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    recruiter: Optional[User] = Relationship(back_populates="jobs")
    applications: List["Application"] = Relationship(back_populates="job")

class Application(SQLModel, table=True):
    __tablename__ = "applications"

    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: int = Field(foreign_key="jobs.id")
    student_id: int = Field(foreign_key="users.id")
    resume_url: str
    cover_letter: Optional[str] = None
    status: str = Field(default="pending")  # pending, reviewed, accepted, rejected
    applied_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    job: Optional[Job] = Relationship(back_populates="applications")
    student: Optional[User] = Relationship(back_populates="applications")

class CollaborationPost(SQLModel, table=True):
    __tablename__ = "collaboration_posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="users.id")
    title: str
    description: str
    required_skills: Optional[str] = None
    project_type: Optional[str] = None
    duration: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    author: Optional[User] = Relationship(back_populates="collaboration_posts")

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    participant1_id: int = Field(foreign_key="users.id")
    participant2_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id")
    sender_id: int = Field(foreign_key="users.id")
    content: str
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
    sender: Optional[User] = Relationship(back_populates="sent_messages")

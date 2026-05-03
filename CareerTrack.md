CareerTrack – Functional Specification (Spec‑Driven Development)

# **Project Overview**

CareerTrack is a web platform that helps students build professional profiles, discover internships or jobs, find collaborators, and communicate with recruiters or other students.

 

Technology Stack

Backend: FastAPI (Python)

Database: PostgreSQL (Neon)

ORM: SQLModel

File Storage: Cloud storage (for resume PDFs)

Frontend: React / Next.js

 

Development will occur in three phases:

1\. Backend Development

2\. Frontend Development

3\. Integration

# **Phase 1 – Backend Development (FastAPI \+ PostgreSQL)**

Goal: Build database models and API endpoints first and test using FastAPI Swagger.

 

Swagger testing URL:

http://localhost:8000/docs

 

Database Tables:

Users

Profiles

Skills

StudentSkills

Projects

Certifications

Jobs

Applications

CollaborationPosts

Conversations

Messages

 

Resume Handling:

• Resume must be PDF

• File uploaded to cloud storage

• Database stores resume\_url

• Recruiters download resume via stored URL

 

Authentication Endpoints:

POST /register

POST /login

POST /logout

 

Profile Endpoints:

GET /profile/{user\_id}

PUT /profile/update

POST /profile/skills

POST /profile/projects

POST /profile/certifications

 

Job Endpoints:

POST /jobs/create

GET /jobs

GET /jobs/{job\_id}

GET /jobs/filter

 

Application Endpoints:

POST /jobs/{job\_id}/apply

GET /jobs/{job\_id}/applicants

 

Collaboration Endpoints:

POST /collaboration/create

GET /collaboration

 

Messaging Endpoints:

POST /messages/send

GET /messages/conversation/{conversation\_id}

GET /messages/conversations

 

Backend Completion Criteria:

• APIs working in Swagger

• Database inserts correctly

• Authentication works

• Resume upload returns URL

• Duplicate job applications blocked

# **Phase 2 – Frontend Development**

Goal: Build user interface that consumes backend APIs.

 

Pages Required:

 

Landing Page

• Platform introduction

• Register button

• Login button

 

Authentication Pages

• Register

• Login

 

Student Dashboard

Sidebar Links:

Dashboard

My Profile

Jobs

Collaboration

Messages

Logout

 

Dashboard shows:

• Total job applications

• Collaboration posts

• Messages received

 

Profile Page

Sections:

• Profile header

• About

• Skills (tags)

• Projects (cards)

• Certifications

• Resume upload

 

Jobs Page

• Search bar

• Filter panel

• Job cards

 

Apply Job Form

• Upload Resume (PDF)

• Submit Application

 

Collaboration Page

Cards include:

• Title

• Description

• Skills needed

• Posted by

• Message button

 

Messaging Page

Two‑panel layout:

Left: Conversation list

Right: Chat window

 

Frontend Completion Criteria:

• All pages render correctly

• Navigation works

• Form validation works

• Resume upload UI functional

# **Phase 3 – Integration**

Goal: Connect frontend with backend APIs.

 

API Communication:

Use fetch() or axios to call FastAPI endpoints.

 

Example Calls:

POST /login

GET /jobs

POST /jobs/{job\_id}/apply

 

Authentication Integration:

• Store JWT token after login

• Attach token to API requests

• Protect dashboard routes

 

Resume Upload Flow:

Student selects resume

→ Frontend sends file

→ Backend uploads to storage

→ Storage returns URL

→ Application saved with resume\_url

 

End‑to‑End Testing:

 

Student Flow:

Register

Create profile

Browse jobs

Apply for job

Upload resume

 

Recruiter Flow:

Register

Post job

View applicants

Download resumes

 

Messaging Flow:

Student sends message

Recruiter replies

 

Project Completion Criteria:

• Backend APIs functional

• Frontend UI working

• Frontend connected to backend

• Core features operational


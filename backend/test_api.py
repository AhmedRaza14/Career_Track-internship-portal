"""
CareerTrack API Test Script
Tests all Phase 1 endpoints to verify functionality
"""

import requests
import json
from typing import Dict, Optional

BASE_URL = "http://localhost:8001"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message: str):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message: str):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_section(message: str):
    print(f"\n{Colors.YELLOW}{'='*60}")
    print(f"{message}")
    print(f"{'='*60}{Colors.END}\n")

class APITester:
    def __init__(self):
        self.student_token: Optional[str] = None
        self.recruiter_token: Optional[str] = None
        self.student_id: Optional[int] = None
        self.recruiter_id: Optional[int] = None
        self.job_id: Optional[int] = None
        self.collaboration_id: Optional[int] = None
        self.conversation_id: Optional[int] = None

    def test_root(self):
        """Test root endpoint"""
        print_info("Testing root endpoint...")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print_success("Root endpoint working")
            return True
        else:
            print_error(f"Root endpoint failed: {response.status_code}")
            return False

    def test_register_student(self):
        """Test student registration"""
        print_info("Testing student registration...")
        data = {
            "email": "student@test.com",
            "password": "password123",
            "role": "student",
            "full_name": "John Doe"
        }
        response = requests.post(f"{BASE_URL}/register", json=data)
        if response.status_code == 201:
            result = response.json()
            self.student_token = result["access_token"]
            self.student_id = result["user_id"]
            print_success(f"Student registered successfully (ID: {self.student_id})")
            return True
        else:
            print_error(f"Student registration failed: {response.text}")
            return False

    def test_register_recruiter(self):
        """Test recruiter registration"""
        print_info("Testing recruiter registration...")
        data = {
            "email": "recruiter@company.com",
            "password": "password123",
            "role": "recruiter",
            "full_name": "Jane Smith"
        }
        response = requests.post(f"{BASE_URL}/register", json=data)
        if response.status_code == 201:
            result = response.json()
            self.recruiter_token = result["access_token"]
            self.recruiter_id = result["user_id"]
            print_success(f"Recruiter registered successfully (ID: {self.recruiter_id})")
            return True
        else:
            print_error(f"Recruiter registration failed: {response.text}")
            return False

    def test_login(self):
        """Test login"""
        print_info("Testing login...")
        data = {
            "username": "student@test.com",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/login", data=data)
        if response.status_code == 200:
            print_success("Login successful")
            return True
        else:
            print_error(f"Login failed: {response.text}")
            return False

    def test_get_profile(self):
        """Test get profile"""
        print_info("Testing get profile...")
        response = requests.get(f"{BASE_URL}/profile/{self.student_id}")
        if response.status_code == 200:
            print_success("Profile retrieved successfully")
            return True
        else:
            print_error(f"Get profile failed: {response.text}")
            return False

    def test_update_profile(self):
        """Test update profile"""
        print_info("Testing update profile...")
        headers = {"Authorization": f"Bearer {self.student_token}"}
        data = {
            "bio": "Computer Science student passionate about web development",
            "education": "BS Computer Science",
            "location": "New York, NY",
            "phone": "+1234567890"
        }
        response = requests.put(f"{BASE_URL}/profile/update", json=data, headers=headers)
        if response.status_code == 200:
            print_success("Profile updated successfully")
            return True
        else:
            print_error(f"Update profile failed: {response.text}")
            return False

    def test_add_skill(self):
        """Test add skill"""
        print_info("Testing add skill...")
        headers = {"Authorization": f"Bearer {self.student_token}"}
        data = {
            "skill_name": "Python",
            "proficiency_level": "advanced"
        }
        response = requests.post(f"{BASE_URL}/profile/skills", json=data, headers=headers)
        if response.status_code == 200:
            print_success("Skill added successfully")
            return True
        else:
            print_error(f"Add skill failed: {response.text}")
            return False

    def test_add_project(self):
        """Test add project"""
        print_info("Testing add project...")
        headers = {"Authorization": f"Bearer {self.student_token}"}
        data = {
            "title": "E-commerce Website",
            "description": "Built a full-stack e-commerce platform",
            "technologies": "React, Node.js, MongoDB",
            "github_url": "https://github.com/johndoe/ecommerce"
        }
        response = requests.post(f"{BASE_URL}/profile/projects", json=data, headers=headers)
        if response.status_code == 200:
            print_success("Project added successfully")
            return True
        else:
            print_error(f"Add project failed: {response.text}")
            return False

    def test_add_certification(self):
        """Test add certification"""
        print_info("Testing add certification...")
        headers = {"Authorization": f"Bearer {self.student_token}"}
        data = {
            "title": "AWS Certified Developer",
            "issuing_organization": "Amazon Web Services",
            "credential_url": "https://aws.amazon.com/certification"
        }
        response = requests.post(f"{BASE_URL}/profile/certifications", json=data, headers=headers)
        if response.status_code == 200:
            print_success("Certification added successfully")
            return True
        else:
            print_error(f"Add certification failed: {response.text}")
            return False

    def test_create_job(self):
        """Test create job"""
        print_info("Testing create job...")
        headers = {"Authorization": f"Bearer {self.recruiter_token}"}
        data = {
            "title": "Software Engineer Intern",
            "company": "Tech Corp",
            "description": "Looking for talented software engineering interns",
            "job_type": "internship",
            "location": "Remote",
            "salary_range": "$20-30/hour",
            "required_skills": "Python, FastAPI, React",
            "experience_level": "Entry Level"
        }
        response = requests.post(f"{BASE_URL}/jobs/create", json=data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            self.job_id = result["id"]
            print_success(f"Job created successfully (ID: {self.job_id})")
            return True
        else:
            print_error(f"Create job failed: {response.text}")
            return False

    def test_get_jobs(self):
        """Test get all jobs"""
        print_info("Testing get all jobs...")
        response = requests.get(f"{BASE_URL}/jobs")
        if response.status_code == 200:
            jobs = response.json()
            print_success(f"Retrieved {len(jobs)} job(s)")
            return True
        else:
            print_error(f"Get jobs failed: {response.text}")
            return False

    def test_get_job_by_id(self):
        """Test get specific job"""
        print_info("Testing get job by ID...")
        response = requests.get(f"{BASE_URL}/jobs/{self.job_id}")
        if response.status_code == 200:
            print_success("Job retrieved successfully")
            return True
        else:
            print_error(f"Get job by ID failed: {response.text}")
            return False

    def test_filter_jobs(self):
        """Test filter jobs"""
        print_info("Testing filter jobs...")
        params = {"job_type": "internship"}
        response = requests.get(f"{BASE_URL}/jobs/filter", params=params)
        if response.status_code == 200:
            jobs = response.json()
            print_success(f"Filtered jobs: {len(jobs)} result(s)")
            return True
        else:
            print_error(f"Filter jobs failed: {response.text}")
            return False

    def test_create_collaboration(self):
        """Test create collaboration post"""
        print_info("Testing create collaboration...")
        headers = {"Authorization": f"Bearer {self.student_token}"}
        data = {
            "title": "Looking for React Developer",
            "description": "Need a frontend developer for a startup project",
            "required_skills": "React, TypeScript, Tailwind CSS",
            "project_type": "Web Application",
            "duration": "3 months"
        }
        response = requests.post(f"{BASE_URL}/collaboration/create", json=data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            self.collaboration_id = result["id"]
            print_success(f"Collaboration created successfully (ID: {self.collaboration_id})")
            return True
        else:
            print_error(f"Create collaboration failed: {response.text}")
            return False

    def test_get_collaborations(self):
        """Test get all collaborations"""
        print_info("Testing get all collaborations...")
        response = requests.get(f"{BASE_URL}/collaboration")
        if response.status_code == 200:
            collabs = response.json()
            print_success(f"Retrieved {len(collabs)} collaboration(s)")
            return True
        else:
            print_error(f"Get collaborations failed: {response.text}")
            return False

    def test_send_message(self):
        """Test send message"""
        print_info("Testing send message...")
        headers = {"Authorization": f"Bearer {self.student_token}"}
        data = {
            "receiver_id": self.recruiter_id,
            "content": "Hello! I'm interested in the Software Engineer Intern position."
        }
        response = requests.post(f"{BASE_URL}/messages/send", json=data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            self.conversation_id = result["conversation_id"]
            print_success("Message sent successfully")
            return True
        else:
            print_error(f"Send message failed: {response.text}")
            return False

    def test_get_conversations(self):
        """Test get all conversations"""
        print_info("Testing get conversations...")
        headers = {"Authorization": f"Bearer {self.student_token}"}
        response = requests.get(f"{BASE_URL}/messages/conversations", headers=headers)
        if response.status_code == 200:
            convs = response.json()
            print_success(f"Retrieved {len(convs)} conversation(s)")
            return True
        else:
            print_error(f"Get conversations failed: {response.text}")
            return False

    def test_get_conversation_messages(self):
        """Test get conversation messages"""
        print_info("Testing get conversation messages...")
        headers = {"Authorization": f"Bearer {self.student_token}"}
        response = requests.get(f"{BASE_URL}/messages/conversation/{self.conversation_id}", headers=headers)
        if response.status_code == 200:
            messages = response.json()
            print_success(f"Retrieved {len(messages)} message(s)")
            return True
        else:
            print_error(f"Get conversation messages failed: {response.text}")
            return False

    def run_all_tests(self):
        """Run all tests"""
        print_section("CareerTrack API Test Suite")
        print_info(f"Testing API at: {BASE_URL}")

        tests = [
            ("Root Endpoint", self.test_root),
            ("Register Student", self.test_register_student),
            ("Register Recruiter", self.test_register_recruiter),
            ("Login", self.test_login),
            ("Get Profile", self.test_get_profile),
            ("Update Profile", self.test_update_profile),
            ("Add Skill", self.test_add_skill),
            ("Add Project", self.test_add_project),
            ("Add Certification", self.test_add_certification),
            ("Create Job", self.test_create_job),
            ("Get All Jobs", self.test_get_jobs),
            ("Get Job by ID", self.test_get_job_by_id),
            ("Filter Jobs", self.test_filter_jobs),
            ("Create Collaboration", self.test_create_collaboration),
            ("Get Collaborations", self.test_get_collaborations),
            ("Send Message", self.test_send_message),
            ("Get Conversations", self.test_get_conversations),
            ("Get Conversation Messages", self.test_get_conversation_messages),
        ]

        passed = 0
        failed = 0

        for test_name, test_func in tests:
            print_section(f"Test: {test_name}")
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print_error(f"Test crashed: {str(e)}")
                failed += 1

        print_section("Test Results")
        print(f"Total Tests: {len(tests)}")
        print_success(f"Passed: {passed}")
        if failed > 0:
            print_error(f"Failed: {failed}")
        else:
            print_success("All tests passed! ✨")

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         CareerTrack API - Phase 1 Test Suite             ║
    ║                                                           ║
    ║  Make sure the backend server is running on port 8001    ║
    ║  Run: start.bat (Windows) or ./start.sh (Linux/Mac)      ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    try:
        tester = APITester()
        tester.run_all_tests()
    except requests.exceptions.ConnectionError:
        print_error("\nCannot connect to the API server!")
        print_info("Please make sure the backend is running on http://localhost:8001")
        print_info("Run: start.bat (Windows) or ./start.sh (Linux/Mac)")
    except KeyboardInterrupt:
        print_info("\n\nTest suite interrupted by user")

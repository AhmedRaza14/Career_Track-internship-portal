"""
CareerTrack Backend - Complete API Test Suite
Tests all 18 endpoints with real data
"""

import requests
import json
from typing import Optional
import time

BASE_URL = "http://localhost:8001"
TIMESTAMP = int(time.time())

class APITester:
    def __init__(self):
        self.student_token: Optional[str] = None
        self.recruiter_token: Optional[str] = None
        self.student_id: Optional[int] = None
        self.recruiter_id: Optional[int] = None
        self.job_id: Optional[int] = None
        self.collaboration_id: Optional[int] = None
        self.conversation_id: Optional[int] = None
        self.passed = 0
        self.failed = 0

    def print_test(self, name: str, passed: bool, details: str = ""):
        if passed:
            print(f"[PASS] {name}")
            self.passed += 1
        else:
            print(f"[FAIL] {name}")
            if details:
                print(f"   Error: {details}")
            self.failed += 1

    def test_root(self):
        """Test root endpoint"""
        try:
            response = requests.get(f"{BASE_URL}/")
            self.print_test("GET / - Root endpoint", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("GET / - Root endpoint", False, str(e))
            return False

    def test_register_student(self):
        """Test student registration"""
        try:
            data = {
                "email": f"student{TIMESTAMP}@test.com",
                "password": "password123",
                "role": "student",
                "full_name": "John Doe"
            }
            response = requests.post(f"{BASE_URL}/register", json=data)
            if response.status_code == 201:
                result = response.json()
                self.student_token = result["access_token"]
                self.student_id = result["user_id"]
                self.print_test("POST /register - Register student", True)
                return True
            else:
                self.print_test("POST /register - Register student", False, response.text)
                return False
        except Exception as e:
            self.print_test("POST /register - Register student", False, str(e))
            return False

    def test_register_recruiter(self):
        """Test recruiter registration"""
        try:
            data = {
                "email": f"recruiter{TIMESTAMP}@company.com",
                "password": "password123",
                "role": "recruiter",
                "full_name": "Jane Smith"
            }
            response = requests.post(f"{BASE_URL}/register", json=data)
            if response.status_code == 201:
                result = response.json()
                self.recruiter_token = result["access_token"]
                self.recruiter_id = result["user_id"]
                self.print_test("POST /register - Register recruiter", True)
                return True
            else:
                self.print_test("POST /register - Register recruiter", False, response.text)
                return False
        except Exception as e:
            self.print_test("POST /register - Register recruiter", False, str(e))
            return False

    def test_login(self):
        """Test login"""
        try:
            data = {
                "username": f"student{TIMESTAMP}@test.com",
                "password": "password123"
            }
            response = requests.post(f"{BASE_URL}/login", data=data)
            self.print_test("POST /login - Login", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("POST /login - Login", False, str(e))
            return False

    def test_logout(self):
        """Test logout"""
        try:
            headers = {"Authorization": f"Bearer {self.student_token}"}
            response = requests.post(f"{BASE_URL}/logout", headers=headers)
            self.print_test("POST /logout - Logout", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("POST /logout - Logout", False, str(e))
            return False

    def test_get_profile(self):
        """Test get profile"""
        try:
            response = requests.get(f"{BASE_URL}/profile/{self.student_id}")
            self.print_test("GET /profile/{user_id} - Get profile", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("GET /profile/{user_id} - Get profile", False, str(e))
            return False

    def test_update_profile(self):
        """Test update profile"""
        try:
            headers = {"Authorization": f"Bearer {self.student_token}"}
            data = {
                "bio": "Computer Science student passionate about web development",
                "education": "BS Computer Science - University",
                "location": "New York, NY",
                "phone": "+1234567890",
                "linkedin_url": "https://linkedin.com/in/johndoe",
                "github_url": "https://github.com/johndoe"
            }
            response = requests.put(f"{BASE_URL}/profile/update", json=data, headers=headers)
            self.print_test("PUT /profile/update - Update profile", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("PUT /profile/update - Update profile", False, str(e))
            return False

    def test_add_skill(self):
        """Test add skill"""
        try:
            headers = {"Authorization": f"Bearer {self.student_token}"}
            data = {
                "skill_name": "Python",
                "proficiency_level": "advanced"
            }
            response = requests.post(f"{BASE_URL}/profile/skills", json=data, headers=headers)
            self.print_test("POST /profile/skills - Add skill", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("POST /profile/skills - Add skill", False, str(e))
            return False

    def test_add_project(self):
        """Test add project"""
        try:
            headers = {"Authorization": f"Bearer {self.student_token}"}
            data = {
                "title": "E-commerce Website",
                "description": "Built a full-stack e-commerce platform with React and Node.js",
                "technologies": "React, Node.js, MongoDB, Express",
                "github_url": "https://github.com/johndoe/ecommerce"
            }
            response = requests.post(f"{BASE_URL}/profile/projects", json=data, headers=headers)
            self.print_test("POST /profile/projects - Add project", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("POST /profile/projects - Add project", False, str(e))
            return False

    def test_add_certification(self):
        """Test add certification"""
        try:
            headers = {"Authorization": f"Bearer {self.student_token}"}
            data = {
                "title": "AWS Certified Developer",
                "issuing_organization": "Amazon Web Services",
                "credential_url": "https://aws.amazon.com/certification"
            }
            response = requests.post(f"{BASE_URL}/profile/certifications", json=data, headers=headers)
            self.print_test("POST /profile/certifications - Add certification", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("POST /profile/certifications - Add certification", False, str(e))
            return False

    def test_create_job(self):
        """Test create job"""
        try:
            headers = {"Authorization": f"Bearer {self.recruiter_token}"}
            data = {
                "title": "Software Engineer Intern",
                "company": "Tech Corp",
                "description": "Looking for talented software engineering interns to join our team",
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
                self.print_test("POST /jobs/create - Create job", True)
                return True
            else:
                self.print_test("POST /jobs/create - Create job", False, response.text)
                return False
        except Exception as e:
            self.print_test("POST /jobs/create - Create job", False, str(e))
            return False

    def test_get_jobs(self):
        """Test get all jobs"""
        try:
            response = requests.get(f"{BASE_URL}/jobs")
            self.print_test("GET /jobs - Get all jobs", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("GET /jobs - Get all jobs", False, str(e))
            return False

    def test_get_job_by_id(self):
        """Test get specific job"""
        try:
            response = requests.get(f"{BASE_URL}/jobs/{self.job_id}")
            self.print_test("GET /jobs/{job_id} - Get job by ID", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("GET /jobs/{job_id} - Get job by ID", False, str(e))
            return False

    def test_filter_jobs(self):
        """Test filter jobs"""
        try:
            params = {"job_type": "internship"}
            response = requests.get(f"{BASE_URL}/jobs/filter", params=params)
            self.print_test("GET /jobs/filter - Filter jobs", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("GET /jobs/filter - Filter jobs", False, str(e))
            return False

    def test_create_collaboration(self):
        """Test create collaboration post"""
        try:
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
                self.print_test("POST /collaboration/create - Create collaboration", True)
                return True
            else:
                self.print_test("POST /collaboration/create - Create collaboration", False, response.text)
                return False
        except Exception as e:
            self.print_test("POST /collaboration/create - Create collaboration", False, str(e))
            return False

    def test_get_collaborations(self):
        """Test get all collaborations"""
        try:
            response = requests.get(f"{BASE_URL}/collaboration")
            self.print_test("GET /collaboration - Get all collaborations", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("GET /collaboration - Get all collaborations", False, str(e))
            return False

    def test_send_message(self):
        """Test send message"""
        try:
            headers = {"Authorization": f"Bearer {self.student_token}"}
            data = {
                "receiver_id": self.recruiter_id,
                "content": "Hello! I'm interested in the Software Engineer Intern position."
            }
            response = requests.post(f"{BASE_URL}/messages/send", json=data, headers=headers)
            if response.status_code == 201:
                result = response.json()
                self.conversation_id = result["conversation_id"]
                self.print_test("POST /messages/send - Send message", True)
                return True
            else:
                self.print_test("POST /messages/send - Send message", False, response.text)
                return False
        except Exception as e:
            self.print_test("POST /messages/send - Send message", False, str(e))
            return False

    def test_get_conversations(self):
        """Test get all conversations"""
        try:
            headers = {"Authorization": f"Bearer {self.student_token}"}
            response = requests.get(f"{BASE_URL}/messages/conversations", headers=headers)
            self.print_test("GET /messages/conversations - Get conversations", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("GET /messages/conversations - Get conversations", False, str(e))
            return False

    def test_get_conversation_messages(self):
        """Test get conversation messages"""
        try:
            headers = {"Authorization": f"Bearer {self.student_token}"}
            response = requests.get(f"{BASE_URL}/messages/conversation/{self.conversation_id}", headers=headers)
            self.print_test("GET /messages/conversation/{id} - Get messages", response.status_code == 200)
            return response.status_code == 200
        except Exception as e:
            self.print_test("GET /messages/conversation/{id} - Get messages", False, str(e))
            return False

    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("CareerTrack Backend - Complete API Test Suite")
        print("="*70 + "\n")

        print("Testing Backend at:", BASE_URL)
        print()

        # Test in order
        print("AUTHENTICATION ENDPOINTS (3)")
        print("-" * 70)
        self.test_root()
        self.test_register_student()
        self.test_register_recruiter()
        self.test_login()
        self.test_logout()
        print()

        print("PROFILE ENDPOINTS (5)")
        print("-" * 70)
        self.test_get_profile()
        self.test_update_profile()
        self.test_add_skill()
        self.test_add_project()
        self.test_add_certification()
        print()

        print("JOB ENDPOINTS (4)")
        print("-" * 70)
        self.test_create_job()
        self.test_get_jobs()
        self.test_get_job_by_id()
        self.test_filter_jobs()
        print()

        print("COLLABORATION ENDPOINTS (2)")
        print("-" * 70)
        self.test_create_collaboration()
        self.test_get_collaborations()
        print()

        print("MESSAGING ENDPOINTS (3)")
        print("-" * 70)
        self.test_send_message()
        self.test_get_conversations()
        self.test_get_conversation_messages()
        print()

        # Summary
        print("="*70)
        print("TEST RESULTS")
        print("="*70)
        total = self.passed + self.failed
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")

        if self.failed == 0:
            print("\nALL TESTS PASSED! Backend is working perfectly!")
        else:
            print(f"\n{self.failed} test(s) failed. Check errors above.")
        print("="*70 + "\n")

if __name__ == "__main__":
    try:
        tester = APITester()
        tester.run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Cannot connect to the API server!")
        print("Please make sure the backend is running on http://localhost:8001")
        print("Run: .venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001")
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Test suite interrupted by user")

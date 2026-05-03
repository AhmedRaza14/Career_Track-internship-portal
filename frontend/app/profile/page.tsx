'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import styles from '../../styles/profile.module.css';

interface Profile {
  bio: string;
  location: string;
  linkedin_url: string;
  github_url: string;
  resume_url: string;
}

interface Skill {
  id: number;
  skill_name: string;
}

interface Project {
  id: number;
  title: string;
  description: string;
  project_url: string;
}

interface Certification {
  id: number;
  title: string;
  issuer: string;
  issue_date: string;
}

export default function ProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [certifications, setCertifications] = useState<Certification[]>([]);
  const [loading, setLoading] = useState(true);
  const [userName, setUserName] = useState('');
  const [userEmail, setUserEmail] = useState('');
  const [profilePicture, setProfilePicture] = useState('');
  const [userRole, setUserRole] = useState('');

  const [showSkillModal, setShowSkillModal] = useState(false);
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [showCertModal, setShowCertModal] = useState(false);
  const [showProfileModal, setShowProfileModal] = useState(false);

  const [newSkill, setNewSkill] = useState('');
  const [newProject, setNewProject] = useState({ title: '', description: '', project_url: '' });
  const [newCert, setNewCert] = useState({ title: '', issuer: '', issue_date: '' });
  const [profileForm, setProfileForm] = useState({ bio: '', location: '', linkedin_url: '', github_url: '', phone: '', education: '', portfolio_url: '' });

  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [uploadingResume, setUploadingResume] = useState(false);

  const [profilePictureFile, setProfilePictureFile] = useState<File | null>(null);
  const [uploadingProfilePicture, setUploadingProfilePicture] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');
    const role = localStorage.getItem('role');

    if (!token || !userId) {
      router.push('/login');
      return;
    }

    if (role) {
      setUserRole(role);
    }

    fetchProfileData(token, userId);
  }, [router]);

  const fetchProfileData = async (token: string, userId: string) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };

      const profileResponse = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/profile/${userId}`, { headers });
      const data = profileResponse.data;

      setUserName(data.user.full_name);
      setUserEmail(data.user.email);
      setProfilePicture(data.user.profile_picture || '');
      setProfile(data.profile);
      setSkills(data.skills || []);
      setProjects(data.projects || []);
      setCertifications(data.certifications || []);

      if (data.profile) {
        setProfileForm({
          bio: data.profile.bio || '',
          location: data.profile.location || '',
          linkedin_url: data.profile.linkedin_url || '',
          github_url: data.profile.github_url || '',
          phone: data.profile.phone || '',
          education: data.profile.education || '',
          portfolio_url: data.profile.portfolio_url || '',
        });
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('user_id');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.put(`${process.env.NEXT_PUBLIC_API_BASE_URL}/profile/update`, profileForm, { headers });

      setShowProfileModal(false);
      // Re-fetch profile data to update UI
      if (token && userId) {
        await fetchProfileData(token, userId);
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile');
    }
  };

  const handleAddSkill = async () => {
    if (!newSkill.trim()) return;

    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('user_id');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/profile/skills`, { skill_name: newSkill }, { headers });

      setNewSkill('');
      setShowSkillModal(false);
      // Re-fetch profile data to update UI
      if (token && userId) {
        await fetchProfileData(token, userId);
      }
    } catch (error) {
      console.error('Error adding skill:', error);
      alert('Failed to add skill');
    }
  };

  const handleAddProject = async () => {
    if (!newProject.title.trim()) return;

    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('user_id');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/profile/projects`, newProject, { headers });

      setNewProject({ title: '', description: '', project_url: '' });
      setShowProjectModal(false);
      // Re-fetch profile data to update UI
      if (token && userId) {
        await fetchProfileData(token, userId);
      }
    } catch (error) {
      console.error('Error adding project:', error);
      alert('Failed to add project');
    }
  };

  const handleAddCertification = async () => {
    if (!newCert.title.trim()) return;

    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('user_id');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/profile/certifications`, newCert, { headers });

      setNewCert({ title: '', issuer: '', issue_date: '' });
      setShowCertModal(false);
      // Re-fetch profile data to update UI
      if (token && userId) {
        await fetchProfileData(token, userId);
      }
    } catch (error) {
      console.error('Error adding certification:', error);
      alert('Failed to add certification');
    }
  };

  const handleResumeUpload = async () => {
    if (!resumeFile) return;

    setUploadingResume(true);
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('user_id');
      const formData = new FormData();
      formData.append('resume', resumeFile);

      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/profile/resume`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      alert('Resume uploaded successfully!');
      setResumeFile(null);
      // Re-fetch profile data to update UI
      if (token && userId) {
        await fetchProfileData(token, userId);
      }
    } catch (error) {
      console.error('Error uploading resume:', error);
      alert('Failed to upload resume');
    } finally {
      setUploadingResume(false);
    }
  };

  const handleProfilePictureUpload = async () => {
    if (!profilePictureFile) return;

    setUploadingProfilePicture(true);
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('user_id');
      const formData = new FormData();
      formData.append('picture', profilePictureFile);

      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/profile/picture`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      alert('Profile picture uploaded successfully!');
      setProfilePictureFile(null);
      // Re-fetch profile data to update UI
      if (token && userId) {
        await fetchProfileData(token, userId);
      }
    } catch (error) {
      console.error('Error uploading profile picture:', error);
      alert('Failed to upload profile picture');
    } finally {
      setUploadingProfilePicture(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading profile...</div>;
  }

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  return (
    <div className={styles['profile-container']}>
        <div className={styles['page-header-with-back']}>
          <button
            className={styles['back-button']}
            onClick={() => router.push('/dashboard')}
          >
            ← Back to Dashboard
          </button>
        </div>
      <div className={styles['profile-content-wrapper']}>

        <div className={styles['profile-header']}>
        <div className={styles['profile-avatar']}>
          {profilePicture ? (
            <img src={profilePicture} alt={userName} />
          ) : (
            getInitials(userName)
          )}
        </div>
        <div className={styles['profile-info']}>
          <h1>{userName}</h1>
          <p>{userEmail}</p>
          {profile?.location && <p>📍 {profile.location}</p>}
        </div>
      </div>

      <div className={styles['profile-section']}>
        <div className={styles['section-header']}>
          <h2>Profile Picture</h2>
        </div>
        <div style={{ marginBottom: '20px' }}>
          <p style={{ marginBottom: '15px', color: 'var(--text-secondary)' }}>
            Upload a profile picture (JPG, PNG, or GIF, max 2MB)
          </p>
          <input
            type="file"
            id="profile-picture-upload"
            accept=".jpg,.jpeg,.png,.gif"
            onChange={(e) => setProfilePictureFile(e.target.files?.[0] || null)}
            style={{ display: 'none' }}
          />
          <label htmlFor="profile-picture-upload" className="btn btn-outline" style={{ marginRight: '10px' }}>
            Choose Picture
          </label>
          {profilePictureFile && (
            <>
              <span style={{ marginRight: '10px' }}>{profilePictureFile.name}</span>
              <button
                className="btn btn-primary"
                onClick={handleProfilePictureUpload}
                disabled={uploadingProfilePicture}
              >
                {uploadingProfilePicture ? 'Uploading...' : 'Upload Picture'}
              </button>
            </>
          )}
        </div>
      </div>

      <div className={styles['profile-section']}>
        <div className={styles['section-header']}>
          <h2>{userRole === 'recruiter' ? 'Company Information' : 'About'}</h2>
          <button className="btn btn-outline" onClick={() => setShowProfileModal(true)}>
            Edit Profile
          </button>
        </div>

        {userRole === 'recruiter' ? (
          <>
            <div style={{ marginBottom: '15px' }}>
              <strong>Company Description:</strong>
              <p style={{ marginTop: '5px' }}>{profile?.bio || 'No company description added yet.'}</p>
            </div>

            {profile?.education && (
              <div style={{ marginBottom: '15px' }}>
                <strong>Industry / Company Size:</strong>
                <p style={{ marginTop: '5px' }}>{profile.education}</p>
              </div>
            )}

            {profile?.portfolio_url && (
              <div style={{ marginBottom: '15px' }}>
                <strong>Company Website:</strong>
                <p style={{ marginTop: '5px' }}>
                  <a href={profile.portfolio_url} target="_blank" rel="noopener noreferrer" className={styles['project-link']}>
                    {profile.portfolio_url}
                  </a>
                </p>
              </div>
            )}

            {profile?.phone && (
              <div style={{ marginBottom: '15px' }}>
                <strong>Contact Phone:</strong>
                <p style={{ marginTop: '5px' }}>{profile.phone}</p>
              </div>
            )}

            {profile?.linkedin_url && (
              <div style={{ marginBottom: '15px' }}>
                <strong>LinkedIn:</strong>
                <p style={{ marginTop: '5px' }}>
                  <a href={profile.linkedin_url} target="_blank" rel="noopener noreferrer" className={styles['project-link']}>
                    Company LinkedIn Profile
                  </a>
                </p>
              </div>
            )}
          </>
        ) : (
          <>
            <p>{profile?.bio || 'No bio added yet.'}</p>
            {profile?.linkedin_url && (
              <p style={{ marginTop: '10px' }}>
                <a href={profile.linkedin_url} target="_blank" rel="noopener noreferrer" className={styles['project-link']}>
                  LinkedIn Profile
                </a>
              </p>
            )}
            {profile?.github_url && (
              <p>
                <a href={profile.github_url} target="_blank" rel="noopener noreferrer" className={styles['project-link']}>
                  GitHub Profile
                </a>
              </p>
            )}
          </>
        )}
      </div>

      {userRole === 'student' && (
        <>
          <div className={styles['profile-section']}>
            <div className={styles['section-header']}>
              <h2>Skills</h2>
              <button className="btn btn-primary" onClick={() => setShowSkillModal(true)}>
                Add Skill
              </button>
            </div>
            <div className={styles['skills-container']}>
              {skills.length > 0 ? (
                skills.map((skill) => (
                  <span key={skill.id} className={styles['skill-tag']}>
                    {skill.skill_name}
                  </span>
                ))
              ) : (
                <p style={{ color: 'var(--text-secondary)' }}>No skills added yet.</p>
              )}
            </div>
          </div>

          <div className={styles['profile-section']}>
            <div className={styles['section-header']}>
              <h2>Projects</h2>
              <button className="btn btn-primary" onClick={() => setShowProjectModal(true)}>
                Add Project
              </button>
            </div>
            <div className={styles['projects-grid']}>
              {projects.length > 0 ? (
                projects.map((project) => (
                  <div key={project.id} className={styles['project-card']}>
                    <h3>{project.title}</h3>
                    <p>{project.description}</p>
                    {project.project_url && (
                      <a href={project.project_url} target="_blank" rel="noopener noreferrer" className={styles['project-link']}>
                        View Project →
                      </a>
                    )}
                  </div>
                ))
              ) : (
                <p style={{ color: 'var(--text-secondary)' }}>No projects added yet.</p>
              )}
            </div>
          </div>
        </>
      )}

      {userRole === 'student' && (
        <>
          <div className={styles['profile-section']}>
            <div className={styles['section-header']}>
              <h2>Certifications</h2>
              <button className="btn btn-primary" onClick={() => setShowCertModal(true)}>
                Add Certification
              </button>
            </div>
            <div className={styles['cert-list']}>
              {certifications.length > 0 ? (
                certifications.map((cert) => (
                  <div key={cert.id} className={styles['cert-item']}>
                    <h3>{cert.title}</h3>
                    <p>{cert.issuer} • {new Date(cert.issue_date).toLocaleDateString()}</p>
                  </div>
                ))
              ) : (
                <p style={{ color: 'var(--text-secondary)' }}>No certifications added yet.</p>
              )}
            </div>
          </div>

          <div className={styles['profile-section']}>
            <div className={styles['section-header']}>
              <h2>Resume</h2>
            </div>
            {profile?.resume_url && (
              <div className={styles['resume-info']} style={{ marginBottom: '15px' }}>
                <span>✓ Resume uploaded</span>
                <a
                  href={
                    profile.resume_url.includes('localhost')
                      ? profile.resume_url.replace(/http:\/\/localhost:\d+/, process.env.NEXT_PUBLIC_API_BASE_URL || '')
                      : profile.resume_url.startsWith('http')
                      ? profile.resume_url
                      : `${process.env.NEXT_PUBLIC_API_BASE_URL}${profile.resume_url}`
                  }
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-outline"
                >
                  View Resume
                </a>
              </div>
            )}
            <div className={styles['resume-upload']}>
              <p style={{ marginBottom: '15px', color: 'var(--text-secondary)' }}>
                {profile?.resume_url ? 'Upload a new resume to replace the current one' : 'Upload your resume (PDF only, max 5MB)'}
              </p>
              <input
            type="file"
            id="resume-upload"
            accept=".pdf"
            onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
          />
          <label htmlFor="resume-upload" className="btn btn-outline" style={{ marginRight: '10px' }}>
            Choose File
          </label>
          {resumeFile && (
            <>
              <span style={{ marginRight: '10px' }}>{resumeFile.name}</span>
              <button
                className="btn btn-primary"
                onClick={handleResumeUpload}
                disabled={uploadingResume}
              >
                {uploadingResume ? 'Uploading...' : profile?.resume_url ? 'Update Resume' : 'Upload'}
              </button>
            </>
          )}
        </div>
      </div>
        </>
      )}

      {showProfileModal && (
        <div className={styles['modal-overlay']} onClick={() => setShowProfileModal(false)}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles['modal-header']}>
              <h2>Edit Profile</h2>
              <button className={styles['close-btn']} onClick={() => setShowProfileModal(false)}>×</button>
            </div>
            <div className="form-group">
              <label className="form-label">{userRole === 'recruiter' ? 'Company Description' : 'Bio'}</label>
              <textarea
                className="form-textarea"
                value={profileForm.bio}
                onChange={(e) => setProfileForm({ ...profileForm, bio: e.target.value })}
                placeholder={userRole === 'recruiter' ? 'Tell us about your company...' : 'Tell us about yourself...'}
              />
            </div>
            <div className="form-group">
              <label className="form-label">{userRole === 'recruiter' ? 'Company Location' : 'Location'}</label>
              <input
                type="text"
                className="form-input"
                value={profileForm.location}
                onChange={(e) => setProfileForm({ ...profileForm, location: e.target.value })}
                placeholder="e.g., New York, USA"
              />
            </div>
            {userRole === 'recruiter' ? (
              <>
                <div className="form-group">
                  <label className="form-label">Industry / Company Size</label>
                  <input
                    type="text"
                    className="form-input"
                    value={profileForm.education}
                    onChange={(e) => setProfileForm({ ...profileForm, education: e.target.value })}
                    placeholder="e.g., Technology, 50-100 employees"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Company Website</label>
                  <input
                    type="url"
                    className="form-input"
                    value={profileForm.portfolio_url}
                    onChange={(e) => setProfileForm({ ...profileForm, portfolio_url: e.target.value })}
                    placeholder="https://yourcompany.com"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Contact Phone</label>
                  <input
                    type="tel"
                    className="form-input"
                    value={profileForm.phone}
                    onChange={(e) => setProfileForm({ ...profileForm, phone: e.target.value })}
                    placeholder="+1 (555) 123-4567"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Company LinkedIn URL</label>
                  <input
                    type="url"
                    className="form-input"
                    value={profileForm.linkedin_url}
                    onChange={(e) => setProfileForm({ ...profileForm, linkedin_url: e.target.value })}
                    placeholder="https://linkedin.com/company/yourcompany"
                  />
                </div>
              </>
            ) : (
              <>
                <div className="form-group">
                  <label className="form-label">LinkedIn URL</label>
                  <input
                    type="url"
                    className="form-input"
                    value={profileForm.linkedin_url}
                    onChange={(e) => setProfileForm({ ...profileForm, linkedin_url: e.target.value })}
                    placeholder="https://linkedin.com/in/yourprofile"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">GitHub URL</label>
                  <input
                    type="url"
                    className="form-input"
                    value={profileForm.github_url}
                    onChange={(e) => setProfileForm({ ...profileForm, github_url: e.target.value })}
                    placeholder="https://github.com/yourusername"
                  />
                </div>
              </>
            )}
            <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleUpdateProfile}>
              Save Changes
            </button>
          </div>
        </div>
      )}

      {showSkillModal && (
        <div className={styles['modal-overlay']} onClick={() => setShowSkillModal(false)}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles['modal-header']}>
              <h2>Add Skill</h2>
              <button className={styles['close-btn']} onClick={() => setShowSkillModal(false)}>×</button>
            </div>
            <div className="form-group">
              <label className="form-label">Skill Name</label>
              <input
                type="text"
                className="form-input"
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                placeholder="e.g., JavaScript, Python, React"
              />
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleAddSkill}>
              Add Skill
            </button>
          </div>
        </div>
      )}

      {showProjectModal && (
        <div className={styles['modal-overlay']} onClick={() => setShowProjectModal(false)}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles['modal-header']}>
              <h2>Add Project</h2>
              <button className={styles['close-btn']} onClick={() => setShowProjectModal(false)}>×</button>
            </div>
            <div className="form-group">
              <label className="form-label">Project Title</label>
              <input
                type="text"
                className="form-input"
                value={newProject.title}
                onChange={(e) => setNewProject({ ...newProject, title: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Description</label>
              <textarea
                className="form-textarea"
                value={newProject.description}
                onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Project URL (optional)</label>
              <input
                type="url"
                className="form-input"
                value={newProject.project_url}
                onChange={(e) => setNewProject({ ...newProject, project_url: e.target.value })}
              />
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleAddProject}>
              Add Project
            </button>
          </div>
        </div>
      )}

      {showCertModal && (
        <div className={styles['modal-overlay']} onClick={() => setShowCertModal(false)}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <div className={styles['modal-header']}>
              <h2>Add Certification</h2>
              <button className={styles['close-btn']} onClick={() => setShowCertModal(false)}>×</button>
            </div>
            <div className="form-group">
              <label className="form-label">Certification Title</label>
              <input
                type="text"
                className="form-input"
                value={newCert.title}
                onChange={(e) => setNewCert({ ...newCert, title: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Issuer</label>
              <input
                type="text"
                className="form-input"
                value={newCert.issuer}
                onChange={(e) => setNewCert({ ...newCert, issuer: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Issue Date</label>
              <input
                type="date"
                className="form-input"
                value={newCert.issue_date}
                onChange={(e) => setNewCert({ ...newCert, issue_date: e.target.value })}
              />
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleAddCertification}>
              Add Certification
            </button>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}

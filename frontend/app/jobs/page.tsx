'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import styles from '../../styles/jobs.module.css';

interface Job {
  id: number;
  recruiter_id: number;
  title: string;
  company: string;
  location: string;
  job_type: string;
  salary_range: string;
  description: string;
  required_skills: string;
  created_at: string;
}

export default function JobsPage() {
  const router = useRouter();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filteredJobs, setFilteredJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [role, setRole] = useState('');
  const [currentUserId, setCurrentUserId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [locationFilter, setLocationFilter] = useState('');
  const [jobTypeFilter, setJobTypeFilter] = useState('');
  const [appliedJobIds, setAppliedJobIds] = useState<number[]>([]);

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showApplyModal, setShowApplyModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [showApplicantsModal, setShowApplicantsModal] = useState(false);
  const [applicants, setApplicants] = useState<any[]>([]);

  const [newJob, setNewJob] = useState({
    title: '',
    company: '',
    location: '',
    job_type: 'full-time',
    salary_range: '',
    description: '',
    required_skills: '',
  });

  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [coverLetter, setCoverLetter] = useState('');
  const [applying, setApplying] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userRole = localStorage.getItem('role');
    const userId = localStorage.getItem('user_id');

    if (!token) {
      router.push('/login');
      return;
    }

    if (userRole) {
      setRole(userRole);
    }

    if (userId) {
      setCurrentUserId(parseInt(userId));
    }

    fetchJobs(token);

    // Fetch student's applications if they're a student
    if (userRole === 'student') {
      fetchMyApplications(token);
    }
  }, [router]);

  useEffect(() => {
    filterJobs();
  }, [searchTerm, locationFilter, jobTypeFilter, jobs]);

  const fetchJobs = async (token: string) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/jobs`, { headers });
      setJobs(response.data);
      setFilteredJobs(response.data);
    } catch (error) {
      console.error('Error fetching jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchMyApplications = async (token: string) => {
    try {
      const headers = { Authorization: `Bearer ${token}` };
      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/applications/my`, { headers });
      const applications = response.data;

      // Extract job IDs from applications
      const jobIds = applications.map((app: any) => app.job_id);
      setAppliedJobIds(jobIds);
    } catch (error) {
      console.error('Error fetching applications:', error);
    }
  };

  const filterJobs = () => {
    let filtered = [...jobs];

    if (searchTerm) {
      filtered = filtered.filter(
        (job) =>
          job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          job.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
          job.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (locationFilter) {
      filtered = filtered.filter((job) =>
        job.location.toLowerCase().includes(locationFilter.toLowerCase())
      );
    }

    if (jobTypeFilter) {
      filtered = filtered.filter((job) => job.job_type === jobTypeFilter);
    }

    setFilteredJobs(filtered);
  };

  const handleCreateJob = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/jobs/create`, newJob, { headers });

      setShowCreateModal(false);
      setNewJob({
        title: '',
        company: '',
        location: '',
        job_type: 'full-time',
        salary_range: '',
        description: '',
        required_skills: '',
      });
      fetchJobs(token!);
    } catch (error) {
      console.error('Error creating job:', error);
      alert('Failed to create job');
    }
  };

  const handleApplyJob = async () => {
    if (!resumeFile) {
      alert('Please upload your resume');
      return;
    }

    setApplying(true);
    try {
      const token = localStorage.getItem('token');
      const formData = new FormData();
      formData.append('resume', resumeFile);
      formData.append('cover_letter', coverLetter);

      await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/jobs/${selectedJob?.id}/apply`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      alert('Application submitted successfully!');

      // Add the job ID to appliedJobIds to show "Applied" badge immediately
      if (selectedJob) {
        setAppliedJobIds([...appliedJobIds, selectedJob.id]);
      }

      setShowApplyModal(false);
      setResumeFile(null);
      setCoverLetter('');
      setSelectedJob(null);
    } catch (error: any) {
      console.error('Error applying to job:', error);
      alert(error.response?.data?.detail || 'Failed to submit application');
    } finally {
      setApplying(false);
    }
  };

  const handleViewApplicants = async (jobId: number) => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const response = await axios.get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/jobs/${jobId}/applicants`, { headers });
      setApplicants(response.data);
      setShowApplicantsModal(true);
    } catch (error) {
      console.error('Error fetching applicants:', error);
      alert('Failed to fetch applicants');
    }
  };

  if (loading) {
    return <div className="loading">Loading jobs...</div>;
  }

  return (
    <div className={styles['jobs-container']}>
        <div className={styles['page-header-with-back']}>
          <button
            className={styles['back-button']}
            onClick={() => router.push('/dashboard')}
          >
            ← Back to Dashboard
          </button>
        </div>
      <div className={styles['jobs-content-wrapper']}>

        <div className={styles['jobs-header']}>
        <div>
          <h1>Jobs</h1>
          <p>{role === 'student' ? 'Find your next opportunity' : 'Manage your job postings'}</p>
        </div>
        {role === 'recruiter' && (
          <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
            Post a Job
          </button>
        )}
      </div>

      <div className={styles['search-filter-section']}>
        <div className={styles['search-bar']}>
          <input
            type="text"
            className="form-input"
            placeholder="Search jobs by title, company, or description..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ flex: 1 }}
          />
          <button className="btn btn-primary" onClick={filterJobs}>
            Search
          </button>
        </div>

        <div className={styles.filters}>
          <div className={styles['filter-group']}>
            <label className="form-label">Location</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g., New York"
              value={locationFilter}
              onChange={(e) => setLocationFilter(e.target.value)}
            />
          </div>
          <div className={styles['filter-group']}>
            <label className="form-label">Job Type</label>
            <select
              className="form-select"
              value={jobTypeFilter}
              onChange={(e) => setJobTypeFilter(e.target.value)}
            >
              <option value="">All Types</option>
              <option value="full-time">Full-time</option>
              <option value="part-time">Part-time</option>
              <option value="internship">Internship</option>
              <option value="contract">Contract</option>
            </select>
          </div>
        </div>
      </div>

      {role === 'recruiter' ? (
        <>
          {/* My Jobs Section */}
          {filteredJobs.filter(job => job.recruiter_id === currentUserId).length > 0 && (
            <div style={{ marginBottom: '40px' }}>
              <h2 style={{ marginBottom: '20px', fontSize: '1.5rem' }}>My Job Posts</h2>
              <div className={styles['jobs-grid']}>
                {filteredJobs.filter(job => job.recruiter_id === currentUserId).map((job) => (
                  <div key={job.id} className={styles['job-card']}>
                    <div className={styles['job-header']}>
                      <div>
                        <h2 className={styles['job-title']}>{job.title}</h2>
                        <p className={styles['job-company']}>{job.company}</p>
                      </div>
                      <span className="badge badge-primary">{job.job_type}</span>
                    </div>

                    <div className={styles['job-meta']}>
                      <div className={styles['job-meta-item']}>
                        <span>📍</span>
                        <span>{job.location}</span>
                      </div>
                      <div className={styles['job-meta-item']}>
                        <span>💰</span>
                        <span>{job.salary_range}</span>
                      </div>
                      <div className={styles['job-meta-item']}>
                        <span>📅</span>
                        <span>{new Date(job.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>

                    <p className={styles['job-description']}>
                      {job.description.length > 200
                        ? `${job.description.substring(0, 200)}...`
                        : job.description}
                    </p>

                    <div className={styles['job-footer']}>
                      <div className={styles['job-skills']}>
                        {job.required_skills && job.required_skills.split(',').slice(0, 3).map((req, idx) => (
                          <span key={idx} className={styles['job-skill-tag']}>
                            {req.trim()}
                          </span>
                        ))}
                      </div>
                      <button
                        className="btn btn-primary"
                        onClick={() => handleViewApplicants(job.id)}
                      >
                        View Applicants
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* All Jobs Section */}
          <div>
            <h2 style={{ marginBottom: '20px', fontSize: '1.5rem' }}>All Job Posts</h2>
            {filteredJobs.filter(job => job.recruiter_id !== currentUserId).length > 0 ? (
              <div className={styles['jobs-grid']}>
                {filteredJobs.filter(job => job.recruiter_id !== currentUserId).map((job) => (
                  <div key={job.id} className={styles['job-card']}>
                    <div className={styles['job-header']}>
                      <div>
                        <h2 className={styles['job-title']}>{job.title}</h2>
                        <p className={styles['job-company']}>{job.company}</p>
                      </div>
                      <span className="badge badge-primary">{job.job_type}</span>
                    </div>

                    <div className={styles['job-meta']}>
                      <div className={styles['job-meta-item']}>
                        <span>📍</span>
                        <span>{job.location}</span>
                      </div>
                      <div className={styles['job-meta-item']}>
                        <span>💰</span>
                        <span>{job.salary_range}</span>
                      </div>
                      <div className={styles['job-meta-item']}>
                        <span>📅</span>
                        <span>{new Date(job.created_at).toLocaleDateString()}</span>
                      </div>
                    </div>

                    <p className={styles['job-description']}>
                      {job.description.length > 200
                        ? `${job.description.substring(0, 200)}...`
                        : job.description}
                    </p>

                    <div className={styles['job-footer']}>
                      <div className={styles['job-skills']}>
                        {job.required_skills && job.required_skills.split(',').slice(0, 3).map((req, idx) => (
                          <span key={idx} className={styles['job-skill-tag']}>
                            {req.trim()}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className={styles['empty-state']}>
                <div className={styles['empty-state-icon']}>💼</div>
                <h2>No other jobs available</h2>
                <p>Check back later for new opportunities</p>
              </div>
            )}
          </div>
        </>
      ) : (
        <div className={styles['jobs-grid']}>
          {filteredJobs.length > 0 ? (
            filteredJobs.map((job) => {
              const hasApplied = appliedJobIds.includes(job.id);
              return (
              <div key={job.id} className={styles['job-card']}>
                <div className={styles['job-header']}>
                  <div>
                    <h2 className={styles['job-title']}>{job.title}</h2>
                    <p className={styles['job-company']}>{job.company}</p>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', alignItems: 'flex-end' }}>
                    <span className="badge badge-primary">{job.job_type}</span>
                    {hasApplied && (
                      <span className="badge" style={{ backgroundColor: '#10b981', color: 'white' }}>
                        ✓ Applied
                      </span>
                    )}
                  </div>
                </div>

                <div className={styles['job-meta']}>
                  <div className={styles['job-meta-item']}>
                    <span>📍</span>
                    <span>{job.location}</span>
                  </div>
                  <div className={styles['job-meta-item']}>
                    <span>💰</span>
                    <span>{job.salary_range}</span>
                  </div>
                  <div className={styles['job-meta-item']}>
                    <span>📅</span>
                    <span>{new Date(job.created_at).toLocaleDateString()}</span>
                  </div>
                </div>

                <p className={styles['job-description']}>
                  {job.description.length > 200
                    ? `${job.description.substring(0, 200)}...`
                    : job.description}
                </p>

                <div className={styles['job-footer']}>
                  <div className={styles['job-skills']}>
                    {job.required_skills && job.required_skills.split(',').slice(0, 3).map((req, idx) => (
                      <span key={idx} className={styles['job-skill-tag']}>
                        {req.trim()}
                      </span>
                    ))}
                  </div>
                  <button
                    className={hasApplied ? "btn btn-outline" : "btn btn-primary"}
                    onClick={() => {
                      if (!hasApplied) {
                        setSelectedJob(job);
                        setShowApplyModal(true);
                      }
                    }}
                    disabled={hasApplied}
                    style={hasApplied ? { cursor: 'not-allowed', opacity: 0.6 } : {}}
                  >
                    {hasApplied ? 'Applied' : 'Apply Now'}
                  </button>
                </div>
              </div>
            );
            })
          ) : (
            <div className={styles['empty-state']}>
              <div className={styles['empty-state-icon']}>💼</div>
              <h2>No jobs found</h2>
              <p>Try adjusting your search filters</p>
            </div>
          )}
        </div>
      )}

      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '600px' }}>
            <div className="modal-header">
              <h2>Post a New Job</h2>
              <button className="close-btn" onClick={() => setShowCreateModal(false)}>×</button>
            </div>
            <div className="form-group">
              <label className="form-label">Job Title</label>
              <input
                type="text"
                className="form-input"
                value={newJob.title}
                onChange={(e) => setNewJob({ ...newJob, title: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Company</label>
              <input
                type="text"
                className="form-input"
                value={newJob.company}
                onChange={(e) => setNewJob({ ...newJob, company: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Location</label>
              <input
                type="text"
                className="form-input"
                value={newJob.location}
                onChange={(e) => setNewJob({ ...newJob, location: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Job Type</label>
              <select
                className="form-select"
                value={newJob.job_type}
                onChange={(e) => setNewJob({ ...newJob, job_type: e.target.value })}
              >
                <option value="full-time">Full-time</option>
                <option value="part-time">Part-time</option>
                <option value="internship">Internship</option>
                <option value="contract">Contract</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Salary Range</label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g., $50,000 - $70,000"
                value={newJob.salary_range}
                onChange={(e) => setNewJob({ ...newJob, salary_range: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Description</label>
              <textarea
                className="form-textarea"
                value={newJob.description}
                onChange={(e) => setNewJob({ ...newJob, description: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Requirements (comma-separated)</label>
              <textarea
                className="form-textarea"
                placeholder="e.g., JavaScript, React, Node.js"
                value={newJob.required_skills}
                onChange={(e) => setNewJob({ ...newJob, required_skills: e.target.value })}
              />
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleCreateJob}>
              Post Job
            </button>
          </div>
        </div>
      )}

      {showApplyModal && selectedJob && (
        <div className="modal-overlay" onClick={() => setShowApplyModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Apply to {selectedJob.title}</h2>
              <button className="close-btn" onClick={() => setShowApplyModal(false)}>×</button>
            </div>
            <div className="form-group">
              <label className="form-label">Upload Resume (PDF)</label>
              <input
                type="file"
                accept=".pdf"
                className="form-input"
                onChange={(e) => setResumeFile(e.target.files?.[0] || null)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Cover Letter (optional)</label>
              <textarea
                className="form-textarea"
                value={coverLetter}
                onChange={(e) => setCoverLetter(e.target.value)}
                placeholder="Tell us why you're a great fit..."
              />
            </div>
            <button
              className="btn btn-primary"
              style={{ width: '100%' }}
              onClick={handleApplyJob}
              disabled={applying || !resumeFile}
            >
              {applying ? 'Submitting...' : 'Submit Application'}
            </button>
          </div>
        </div>
      )}

      {showApplicantsModal && (
        <div className="modal-overlay" onClick={() => setShowApplicantsModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '700px' }}>
            <div className="modal-header">
              <h2>Applicants</h2>
              <button className="close-btn" onClick={() => setShowApplicantsModal(false)}>×</button>
            </div>
            {applicants.length > 0 ? (
              <div className={styles['applicants-list']}>
                {applicants.map((applicant) => (
                  <div key={applicant.id} className={styles['applicant-card']}>
                    <div className={styles['applicant-info']}>
                      <h3>{applicant.student_name}</h3>
                      <p>Applied on {new Date(applicant.applied_at).toLocaleDateString()}</p>
                      {applicant.cover_letter && <p style={{ marginTop: '8px' }}>{applicant.cover_letter}</p>}
                    </div>
                    <div className={styles['applicant-actions']}>
                      <a
                        href={
                          applicant.resume_url.includes('localhost')
                            ? applicant.resume_url.replace(/http:\/\/localhost:\d+/, process.env.NEXT_PUBLIC_API_BASE_URL || '')
                            : applicant.resume_url.startsWith('http')
                            ? applicant.resume_url
                            : `${process.env.NEXT_PUBLIC_API_BASE_URL}${applicant.resume_url}`
                        }
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-primary"
                      >
                        View Resume
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ textAlign: 'center', padding: '40px', color: 'var(--text-secondary)' }}>
                No applicants yet
              </p>
            )}
          </div>
        </div>
      )}
    </div>
    </div>
  );
}

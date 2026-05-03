"""
Script to add database indexes for performance optimization
Run this once to add indexes to existing database
"""
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./careertrack.db")
engine = create_engine(DATABASE_URL)

indexes = [
    "CREATE INDEX IF NOT EXISTS idx_jobs_recruiter_id ON jobs(recruiter_id);",
    "CREATE INDEX IF NOT EXISTS idx_jobs_is_active ON jobs(is_active);",
    "CREATE INDEX IF NOT EXISTS idx_applications_job_id ON applications(job_id);",
    "CREATE INDEX IF NOT EXISTS idx_applications_student_id ON applications(student_id);",
    "CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);",
    "CREATE INDEX IF NOT EXISTS idx_collaboration_posts_author_id ON collaboration_posts(author_id);",
    "CREATE INDEX IF NOT EXISTS idx_collaboration_posts_is_active ON collaboration_posts(is_active);",
    "CREATE INDEX IF NOT EXISTS idx_conversations_participant1_id ON conversations(participant1_id);",
    "CREATE INDEX IF NOT EXISTS idx_conversations_participant2_id ON conversations(participant2_id);",
    "CREATE INDEX IF NOT EXISTS idx_conversations_updated_at ON conversations(updated_at);",
    "CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);",
    "CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);",
    "CREATE INDEX IF NOT EXISTS idx_messages_is_read ON messages(is_read);",
    "CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);",
]

print("Adding database indexes...")
with engine.connect() as conn:
    for idx_sql in indexes:
        try:
            conn.execute(text(idx_sql))
            print(f"[OK] {idx_sql.split('idx_')[1].split(' ON')[0]}")
        except Exception as e:
            print(f"[ERROR] {e}")
    conn.commit()

print("\nIndexes added successfully!")

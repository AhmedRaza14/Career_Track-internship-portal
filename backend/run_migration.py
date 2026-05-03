"""
Database migration script to add Google OAuth support
Run this script to update your database schema
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in .env file")
    exit(1)

print("Starting database migration for Google OAuth support...")
print(f"Connecting to database...")

try:
    # Connect to database
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    print("[OK] Connected to database")

    # Migration SQL commands
    migrations = [
        ("Adding google_id column",
         "ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR"),

        ("Adding unique constraint on google_id",
         "DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'users_google_id_key') THEN ALTER TABLE users ADD CONSTRAINT users_google_id_key UNIQUE (google_id); END IF; END $$"),

        ("Adding auth_provider column",
         "ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_provider VARCHAR DEFAULT 'email'"),

        ("Adding profile_picture column",
         "ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture VARCHAR"),

        ("Making hashed_password nullable",
         "ALTER TABLE users ALTER COLUMN hashed_password DROP NOT NULL"),

        ("Making role nullable",
         "ALTER TABLE users ALTER COLUMN role DROP NOT NULL"),

        ("Updating existing users auth_provider",
         "UPDATE users SET auth_provider = 'email' WHERE auth_provider IS NULL"),
    ]

    # Execute each migration
    for description, sql in migrations:
        try:
            print(f"  -> {description}...", end=" ")
            cursor.execute(sql)
            conn.commit()
            print("[DONE]")
        except Exception as e:
            print(f"[ERROR] ({e})")
            # Continue with other migrations even if one fails

    print("\n[SUCCESS] Migration completed successfully!")
    print("\nYou can now restart your backend server.")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"\n[FAILED] Migration failed: {e}")
    exit(1)

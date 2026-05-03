-- Migration script to add Google OAuth support to users table
-- Run this in your PostgreSQL database

-- Add google_id column
ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR;
ALTER TABLE users ADD CONSTRAINT users_google_id_key UNIQUE (google_id);

-- Add auth_provider column
ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_provider VARCHAR DEFAULT 'email';

-- Add profile_picture column
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture VARCHAR;

-- Make hashed_password nullable (for Google OAuth users)
ALTER TABLE users ALTER COLUMN hashed_password DROP NOT NULL;

-- Make role nullable (for Google OAuth users during registration)
ALTER TABLE users ALTER COLUMN role DROP NOT NULL;

-- Update existing users to have auth_provider = 'email'
UPDATE users SET auth_provider = 'email' WHERE auth_provider IS NULL;

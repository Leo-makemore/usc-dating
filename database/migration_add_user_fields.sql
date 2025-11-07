-- Migration: Add new user profile fields
-- Run this after the initial schema to add height, weight, nationality, ethnicity, and photos

-- Add new columns to users table
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS height_cm INTEGER,
ADD COLUMN IF NOT EXISTS weight_kg INTEGER,
ADD COLUMN IF NOT EXISTS nationality VARCHAR(100),
ADD COLUMN IF NOT EXISTS ethnicity VARCHAR(100),
ADD COLUMN IF NOT EXISTS photos TEXT[] DEFAULT ARRAY[]::TEXT[],
ADD COLUMN IF NOT EXISTS profile_completed BOOLEAN DEFAULT FALSE;

-- Add index for profile completion status
CREATE INDEX IF NOT EXISTS idx_users_profile_completed ON users(profile_completed);


# Complete .env Setup Guide

This guide will help you get all the credentials needed for your `.env` file.

---

## 📋 What You Need

Your `.env` file needs these credentials:
```env
DATABASE_URL=postgresql://user:password@host:5432/careertrack
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

---

## 1️⃣ Generate SECRET_KEY (JWT Token Security)

### Method 1: Using Python (Recommended)

Run this command in your terminal:
```bash
cd backend
.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and use it as your SECRET_KEY.

### Method 2: Online Generator

Visit: https://generate-secret.vercel.app/32
- Click "Generate"
- Copy the generated key

**Example:**
```env
SECRET_KEY=xK9mP2nQ5rT8wY1zA4bC7dE0fG3hJ6kL9mN2pQ5rT8w
```

---

## 2️⃣ Get Free PostgreSQL Database (Neon.tech)

### Step-by-Step:

**Step 1: Go to Neon.tech**
- Visit: https://neon.tech
- Click "Sign Up" (top right)

**Step 2: Create Account**
- Sign up with GitHub, Google, or Email
- No credit card required!

**Step 3: Create a New Project**
- After login, click "Create Project"
- Project Name: `careertrack` (or any name you like)
- Region: Choose closest to you (e.g., US East, Europe, Asia)
- PostgreSQL Version: Keep default (16)
- Click "Create Project"

**Step 4: Get Connection String**
- After project is created, you'll see a connection string
- Look for "Connection String" section
- Copy the string that looks like:
  ```
  postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/dbname?sslmode=require
  ```

**Step 5: Add to .env**
```env
DATABASE_URL=postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/careertrack?sslmode=require
```

**Important Notes:**
- ✅ Free tier: 0.5 GB storage, 1 project
- ✅ No credit card needed
- ✅ Always-on database
- ✅ Automatic backups

---

## 3️⃣ Get Free Cloud Storage (Cloudinary)

### Step-by-Step:

**Step 1: Go to Cloudinary**
- Visit: https://cloudinary.com/users/register/free
- Click "Sign Up for Free"

**Step 2: Create Account**
- Fill in:
  - Email address
  - Password
  - Cloud name (e.g., `careertrack-resumes`)
- Click "Create Account"
- Verify your email

**Step 3: Access Dashboard**
- After email verification, login
- You'll be on the Dashboard
- Look for "Account Details" or "API Keys" section

**Step 4: Get Your Credentials**

You'll see three important values:

1. **Cloud Name**
   - Found at top of dashboard
   - Example: `careertrack-resumes`

2. **API Key**
   - Found in "Account Details" section
   - Example: `123456789012345`

3. **API Secret**
   - Click "Reveal" or "Show" next to API Secret
   - Example: `abcdefghijklmnopqrstuvwxyz123456`

**Step 5: Add to .env**
```env
CLOUDINARY_CLOUD_NAME=careertrack-resumes
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
```

**Important Notes:**
- ✅ Free tier: 25 GB storage, 25 GB bandwidth/month
- ✅ No credit card needed
- ✅ Perfect for resume PDFs
- ✅ Automatic CDN delivery

---

## 4️⃣ Complete .env File Example

After getting all credentials, your `.env` file should look like:

```env
# Database Configuration
DATABASE_URL=postgresql://neondb_owner:AbCdEf123@ep-cool-cloud-123456.us-east-2.aws.neon.tech/careertrack?sslmode=require

# JWT Configuration
SECRET_KEY=xK9mP2nQ5rT8wY1zA4bC7dE0fG3hJ6kL9mN2pQ5rT8w
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Cloudinary Configuration (for resume uploads)
CLOUDINARY_CLOUD_NAME=careertrack-resumes
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=abcdefghijklmnopqrstuvwxyz123456
```

---

## 5️⃣ Create Your .env File

**Windows:**
```bash
cd backend
copy .env.example .env
notepad .env
```

**Linux/Mac:**
```bash
cd backend
cp .env.example .env
nano .env
```

Then paste your credentials and save the file.

---

## 6️⃣ Verify Setup

After creating your `.env` file:

1. **Stop the current server** (if running)
2. **Restart the server:**
   ```bash
   cd backend
   .venv\Scripts\activate.bat
   uvicorn app.main:app --reload --port 8001
   ```

3. **Check for errors:**
   - If you see "Application startup complete" → ✅ Success!
   - If you see database errors → Check DATABASE_URL
   - If you see Cloudinary errors → Check CLOUDINARY credentials

---

## 🔧 Troubleshooting

### Database Connection Issues

**Error: "could not connect to server"**
- ✅ Check DATABASE_URL is correct
- ✅ Ensure `?sslmode=require` is at the end
- ✅ Verify Neon project is active

**Error: "password authentication failed"**
- ✅ Copy the connection string again from Neon dashboard
- ✅ Make sure no extra spaces in .env file

### Cloudinary Issues

**Error: "Invalid cloud_name"**
- ✅ Check CLOUDINARY_CLOUD_NAME matches your dashboard
- ✅ No spaces or special characters

**Error: "Invalid API credentials"**
- ✅ Verify API_KEY and API_SECRET are correct
- ✅ Make sure you revealed the secret before copying

---

## 📞 Quick Links

- **Neon Dashboard:** https://console.neon.tech
- **Cloudinary Dashboard:** https://cloudinary.com/console
- **Secret Key Generator:** https://generate-secret.vercel.app/32

---

## ✅ Checklist

Before running your backend, make sure:

- [ ] SECRET_KEY is generated and added
- [ ] DATABASE_URL from Neon is added
- [ ] CLOUDINARY_CLOUD_NAME is added
- [ ] CLOUDINARY_API_KEY is added
- [ ] CLOUDINARY_API_SECRET is added
- [ ] .env file is in the `backend/` directory
- [ ] No extra spaces or quotes around values
- [ ] File is named exactly `.env` (not `.env.txt`)

---

## 🎉 You're Ready!

Once all credentials are in your `.env` file, your backend will:
- ✅ Connect to PostgreSQL database
- ✅ Generate secure JWT tokens
- ✅ Upload resumes to Cloudinary
- ✅ Store all data persistently

Start the server and test at: http://localhost:8001/docs

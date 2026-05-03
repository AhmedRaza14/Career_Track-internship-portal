import os
from fastapi import UploadFile, HTTPException
import shutil
from pathlib import Path

# Get the backend directory (parent of app directory)
BASE_DIR = Path(__file__).resolve().parent.parent

# Create uploads directory if it doesn't exist
UPLOAD_DIR = BASE_DIR / "uploads" / "resumes"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_PICS_DIR = BASE_DIR / "uploads" / "profile_pictures"
PROFILE_PICS_DIR.mkdir(parents=True, exist_ok=True)

async def upload_resume(file: UploadFile) -> str:
    """
    Upload resume PDF to local storage and return the URL
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Read file contents
    contents = await file.read()

    # Validate file size (max 5MB)
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit")

    try:
        # Generate unique filename
        import uuid
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / unique_filename

        # Save file to local storage
        with open(file_path, "wb") as f:
            f.write(contents)

        print(f"File saved to: {file_path}")
        print(f"File exists: {file_path.exists()}")

        # Return relative URL path (will be served by FastAPI static files)
        return f"/uploads/resumes/{unique_filename}"
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

async def upload_profile_picture(file: UploadFile) -> str:
    """
    Upload profile picture to local storage and return the URL
    """
    # Validate file type
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        raise HTTPException(status_code=400, detail="Only image files (JPG, PNG, GIF) are allowed")

    # Read file contents
    contents = await file.read()

    # Validate file size (max 2MB)
    if len(contents) > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 2MB limit")

    try:
        # Generate unique filename
        import uuid
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = PROFILE_PICS_DIR / unique_filename

        # Save file to local storage
        with open(file_path, "wb") as f:
            f.write(contents)

        # Return relative URL path (will be served by FastAPI static files)
        return f"/uploads/profile_pictures/{unique_filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile picture upload failed: {str(e)}")

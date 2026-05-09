import os
from fastapi import UploadFile, HTTPException
import cloudinary
import cloudinary.uploader
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

async def upload_resume(file: UploadFile) -> str:
    """
    Upload resume PDF to Cloudinary and return the URL
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
        # Upload to Cloudinary as image type (allows transformations)
        result = cloudinary.uploader.upload(
            contents,
            resource_type="image",
            format="pdf",
            folder="careertrack/resumes",
            public_id=file.filename.replace('.pdf', ''),
            overwrite=True,
            type="upload",  # Public upload
            access_mode="public"  # Make publicly accessible
        )

        # Return URL with fl_attachment flag removed (forces inline viewing)
        secure_url = result['secure_url']
        # Replace /upload/ with /upload/fl_attachment:false/ to force inline viewing
        if '/upload/' in secure_url:
            secure_url = secure_url.replace('/upload/', '/upload/fl_attachment:false/')

        return secure_url
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

async def upload_profile_picture(file: UploadFile) -> str:
    """
    Upload profile picture to Cloudinary and return the URL
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
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            contents,
            folder="careertrack/profile_pictures",
            overwrite=True,
            type="upload",  # Public upload
            access_mode="public"  # Make publicly accessible
        )

        # Return the secure URL from Cloudinary
        return result['secure_url']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile picture upload failed: {str(e)}")

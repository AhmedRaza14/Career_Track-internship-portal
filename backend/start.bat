@echo off
echo ========================================
echo Starting CareerTrack Backend Server
echo ========================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment not found!
    echo Please run 'setup.bat' first to set up the environment.
    pause
    exit /b 1
)
echo.

echo Checking for .env file...
if not exist .env (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure your settings.
    pause
    exit /b 1
)
echo.

echo Starting FastAPI server on port 8001...
echo Server will be available at: http://localhost:8001
echo API Documentation: http://localhost:8001/docs
echo.
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

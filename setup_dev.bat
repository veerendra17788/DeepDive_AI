@echo off
REM setup_dev.bat - Development Environment Setup Script for Windows

echo 🚀 Setting up DeepDive AI Development Environment...

REM Check Python version
echo 📋 Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%

REM Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo 🔐 Creating .env file...
    echo # Gemini API Configuration > .env
    echo # Get your API key from: https://makersuite.google.com/app/apikey >> .env
    echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
    echo. >> .env
    echo # Groq API Configuration >> .env
    echo # Get your API key from: https://console.groq.com >> .env
    echo GROQ_API_KEY=your_groq_api_key_here >> .env
    echo. >> .env
    echo # Auth Configuration >> .env
    for /f %%i in ('python -c "import secrets; print(secrets.token_hex(32))"') do echo SECRET_KEY=%%i >> .env
    echo ALGORITHM=HS256 >> .env
    echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env
    echo. >> .env
    echo # Development Settings >> .env
    echo DEBUG=True >> .env
    echo HOST=127.0.0.1 >> .env
    echo PORT=8000 >> .env
    echo ⚠️ Please update the API keys in .env file
) else (
    echo ✅ .env file already exists
)

REM Create directories if they don't exist
echo 📁 Creating required directories...
if not exist uploads mkdir uploads
if not exist reports\generated mkdir reports\generated
if not exist logs mkdir logs

echo 🎉 Development environment setup complete!
echo 📝 Next steps:
echo 1. Update API keys in .env file
echo 2. Run: uvicorn app:app --reload
echo 3. Open: http://127.0.0.1:8000
echo 💡 Use 'deactivate' to exit the virtual environment
pause
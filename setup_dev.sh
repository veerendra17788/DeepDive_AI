#!/bin/bash
# setup_dev.sh - Development Environment Setup Script

set -e

echo "🚀 Setting up DeepDive AI Development Environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}📋 Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo -e "${RED}❌ Python not found. Please install Python 3.11+${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Found Python $PYTHON_VERSION${NC}"

# Create virtual environment
echo -e "${BLUE}🔧 Creating virtual environment...${NC}"
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo -e "${BLUE}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}🔐 Creating .env file...${NC}"
    cat > .env << EOL
# Gemini API Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Groq API Configuration
# Get your API key from: https://console.groq.com
GROQ_API_KEY=your_groq_api_key_here

# Auth Configuration
SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Development Settings
DEBUG=True
HOST=127.0.0.1
PORT=8000
EOL
    echo -e "${YELLOW}⚠️  Please update the API keys in .env file${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Create directories if they don't exist
echo -e "${BLUE}📁 Creating required directories...${NC}"
mkdir -p uploads
mkdir -p reports/generated
mkdir -p logs

echo -e "${GREEN}🎉 Development environment setup complete!${NC}"
echo -e "${BLUE}📝 Next steps:${NC}"
echo "1. Update API keys in .env file"
echo "2. Run: uvicorn app:app --reload"
echo "3. Open: http://127.0.0.1:8000"
echo -e "${YELLOW}💡 Use 'deactivate' to exit the virtual environment${NC}"
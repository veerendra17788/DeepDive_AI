# DeepDive AI - Quick Reference Guide

## 🚀 Essential Commands & Configuration

---

## 1. Installation & Setup

### Quick Start (Automated)
```bash
# Windows
setup_dev.bat

# macOS/Linux
chmod +x setup_dev.sh && ./setup_dev.sh
```

### Manual Setup
```bash
# Clone repository
git clone https://github.com/veerendra17788/DeepDive_AI.git
cd DeepDive_AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

---

## 2. Environment Variables

### Required Variables (.env file)
```bash
# AI API Keys
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Authentication
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (optional, defaults to SQLite)
DATABASE_URL=sqlite:///./site.db

# Logging (optional)
LOG_LEVEL=INFO
```

### Get API Keys
- **Gemini**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- **Groq**: [https://console.groq.com](https://console.groq.com)

---

## 3. Running the Application

### Development Server
```bash
# Standard
uvicorn app:app --reload --host 127.0.0.1 --port 8000

# Custom port
uvicorn app:app --reload --port 8001

# Accessible from network
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
# Using Gunicorn (recommended)
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Using Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access Application
- **Local**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Network**: http://YOUR_IP:8000

---

## 4. API Endpoints Reference

### Chat Endpoints

#### **POST /api/chat**
```json
{
  "message": "Your question here",
  "image": "base64_encoded_image (optional)",
  "custom_instruction": "System prompt (optional)",
  "model_name": "gemini-2.0-flash"
}
```

**Response:**
```json
{
  "response": "AI response",
  "history": [...]
}
```

#### **POST /api/clear**
Clears conversation history.

### Research Endpoints

#### **POST /api/online**
Quick online search with AI summary.

```json
{
  "query": "search query",
  "search_engines": ["google", "bing", "duckduckgo"]
}
```

**Response:**
```json
{
  "explanation": "AI summary",
  "references": ["url1", "url2"],
  "history": [...]
}
```

#### **POST /api/deep_research**
Comprehensive iterative research.

```json
{
  "query": "research topic",
  "model_name": "gemini-2.0-flash",
  "search_engines": ["google", "bing", "duckduckgo", "brave", "yahoo", "linkedin"],
  "output_format": "markdown",
  "extract_links": false,
  "extract_emails": false,
  "download_pdf": true,
  "max_iterations": 3
}
```

**Response:**
```json
{
  "report": "Comprehensive markdown report",
  "references": ["url1", "url2"],
  "pdf_url": "/downloads/report.pdf",
  "extracted_data": {...}
}
```

---

## 5. Configuration Options

### Search Engines
```python
SEARCH_ENGINES = [
    "google",       # Google Search
    "duckduckgo",   # DuckDuckGo
    "bing",         # Bing Search
    "yahoo",        # Yahoo Search
    "brave",        # Brave Search
    "linkedin"      # LinkedIn (people search)
]
```

### AI Models
```python
# Gemini Models
"gemini-2.0-flash"                      # Fast, general-purpose
"gemini-2.0-flash-thinking-exp-01-21"   # Enhanced reasoning

# Rate Limits
"gemini-2.0-flash": 15 requests/minute
"gemini-2.0-flash-thinking-exp-01-21": 10 requests/minute
```

### Performance Settings
```python
SNIPPET_LENGTH = 5000                    # Standard content length
DEEP_RESEARCH_SNIPPET_LENGTH = 10000     # Deep research content
MAX_TOKENS_PER_CHUNK = 25000             # Chunk processing limit
REQUEST_TIMEOUT = 60                     # HTTP request timeout (seconds)
MAX_WORKERS = 10                         # Concurrent thread pool size
CACHE_TIMEOUT = 300                      # Cache expiration (5 minutes)
```

---

## 6. Database Commands

### SQLite (Development)
```bash
# View database
sqlite3 site.db

# Common queries
.tables                          # List tables
SELECT * FROM user;              # View users
SELECT * FROM conversation;      # View conversations
SELECT * FROM message;           # View messages
.exit                           # Exit SQLite
```

### PostgreSQL (Production)
```bash
# Connect to database
psql $DATABASE_URL

# Common queries
\dt                             # List tables
SELECT * FROM user;             # View users
\q                              # Exit psql
```

---

## 7. Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_research.py

# Run specific test
pytest tests/test_research.py::test_deep_research
```

### Manual Testing
```bash
# Check API health
curl http://127.0.0.1:8000/

# Test chat endpoint
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'

# Test online search
curl -X POST http://127.0.0.1:8000/api/online \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence"}'
```

---

## 8. Deployment

### Render Deployment
```bash
# 1. Push to GitHub
git add .
git commit -m "Deploy to Render"
git push origin main

# 2. Configure on Render dashboard
# - Connect GitHub repository
# - Set environment variables
# - Deploy automatically
```

### Docker Deployment
```bash
# Build image
docker build -t deepdive-ai .

# Run container
docker run -d -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e GROQ_API_KEY=your_key \
  -e SECRET_KEY=your_secret \
  deepdive-ai

# View logs
docker logs <container_id>

# Stop container
docker stop <container_id>
```

---

## 9. Troubleshooting

### Common Issues

#### **ModuleNotFoundError**
```bash
# Solution
pip install --upgrade pip
pip install -r requirements.txt
```

#### **Permission Denied**
```bash
# Solution (Windows)
pip install --user -r requirements.txt

# Solution (Linux/macOS)
sudo pip install -r requirements.txt
# OR
pip install --user -r requirements.txt
```

#### **Port Already in Use**
```bash
# Solution: Change port
uvicorn app:app --port 8001

# OR kill process using port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS:
lsof -i :8000
kill -9 <PID>
```

#### **API Key Issues**
```bash
# Verify .env file exists
ls -la .env

# Check environment variables are loaded
python debug_env.py

# Ensure no spaces around = in .env
# Correct:   GEMINI_API_KEY=abc123
# Incorrect: GEMINI_API_KEY = abc123
```

#### **Database Errors**
```bash
# Reset database
rm site.db
python -c "from database import init_db; init_db()"

# Check database permissions
ls -l site.db
chmod 644 site.db
```

#### **Rate Limit Errors**
- **Solution**: Wait for rate limit window to reset
- **Alternative**: Switch to different AI model
- **Prevention**: Implement request throttling

---

## 10. Useful Scripts

### Generate Secret Key
```python
# Python
import secrets
print(secrets.token_hex(32))
```

```bash
# Bash (Linux/macOS)
python -c 'import secrets; print(secrets.token_hex(32))'

# PowerShell (Windows)
python -c "import secrets; print(secrets.token_hex(32))"
```

### Check Groq Models
```bash
python check_groq_models.py
```

### Health Check
```bash
python check_health.py
```

### Debug Environment
```bash
python debug_env.py
```

---

## 11. Git Workflow

### Basic Workflow
```bash
# Check status
git status

# Stage changes
git add .

# Commit changes
git commit -m "feat: add new feature"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

### Branch Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: implement new feature"

# Push branch
git push origin feature/new-feature

# Merge to main (after PR approval)
git checkout main
git merge feature/new-feature
git push origin main
```

### Commit Message Convention
```
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Format code
refactor: Refactor code
perf: Improve performance
test: Add tests
chore: Update dependencies
```

---

## 12. Performance Monitoring

### Check Application Performance
```bash
# CPU and memory usage
top
htop  # If installed

# Python profiling
python -m cProfile app.py

# Request timing
time curl http://127.0.0.1:8000/api/chat -X POST -d '{"message":"test"}'
```

### Monitor Logs
```bash
# Tail application logs
tail -f app.log

# Search logs
grep "ERROR" app.log
grep "deep_research" app.log
```

---

## 13. Security Best Practices

### Checklist
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS in production
- [ ] Implement rate limiting
- [ ] Validate all user inputs
- [ ] Use Argon2 for password hashing
- [ ] Rotate JWT secret keys regularly
- [ ] Keep dependencies updated
- [ ] Enable CORS selectively
- [ ] Implement logging and monitoring
- [ ] Regular security audits

### Update Dependencies
```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package_name

# Update all packages (careful!)
pip install --upgrade -r requirements.txt
```

---

## 14. Useful Links

### Documentation
- **FastAPI**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **Gemini API**: [https://ai.google.dev/](https://ai.google.dev/)
- **Groq**: [https://console.groq.com/docs](https://console.groq.com/docs)
- **SQLModel**: [https://sqlmodel.tiangolo.com/](https://sqlmodel.tiangolo.com/)

### Community
- **GitHub Issues**: [Report bugs](https://github.com/veerendra17788/DeepDive_AI/issues)
- **Discussions**: [Community forum](https://github.com/veerendra17788/DeepDive_AI/discussions)

### Support
- **Email**: 21131A05C6@gvpce.ac.in
- **LinkedIn**: [K. Veerendra Kumar](https://www.linkedin.com/in/karri-vamsi-krishna-966537251/)

---

## 15. Keyboard Shortcuts (Web Interface)

| Action | Shortcut |
|--------|----------|
| Send message | `Ctrl + Enter` |
| Clear chat | `Ctrl + Shift + C` |
| New conversation | `Ctrl + N` |
| Toggle dark mode | `Ctrl + D` |
| Focus input | `/` |

---

**Last Updated**: December 29, 2025  
**Version**: 1.0  
**License**: MIT License

---

## Quick Command Summary

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run
uvicorn app:app --reload

# Test
pytest --cov=app

# Deploy
git push origin main

# Monitor
tail -f app.log
```

**Need help?** Check the [complete documentation](COMPLETE_DOCUMENTATION.md) or [research bibliography](RESEARCH_BIBLIOGRAPHY.md).

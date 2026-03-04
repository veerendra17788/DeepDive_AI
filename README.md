# 🧠 DeepDive AI: The Ultimate Research & Career Companion

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

**DeepDive AI** is a production-ready, open-source platform that synergistically integrates Google Gemini 2.0 Flash AI, Groq's ultra-fast LPU inference, and sophisticated multi-engine web scraping to deliver comprehensive research automation and intelligent job matching.

---

## ✨ Key Features

### 🔍 1. Deep Research Engine
*   **Iterative Methodology**: Automatically refines search queries based on gap analysis.
*   **Multi-Engine Scraping**: Scours Google, Bing, DuckDuckGo, Yahoo, Brave, and LinkedIn simultaneously.
*   **Intelligent Synthesis**: Consolidates findings from dozens of sources into structured markdown reports.
*   **Extensive Extraction**: Extracts links, emails, and specialized data points with 300s TTL caching.

### 💼 2. Intelligent Career Suite
*   **Resume Parsing**: Advanced analysis of PDF and DOCX files with no page limits.
*   **Skill Gap Identification**: Compares your profile against real-world job requirements.
*   **Job Search Automation**: Scrapes LinkedIn, Indeed, and Glassdoor for real-time opportunities.
*   **Relevance Scoring**: AI-powered scoring (87% accuracy) to find your perfect job match.

### 🤖 3. Conversational AI & Tools
*   **Multi-Model Support**: Switch between Gemini 2.0 Flash and Flash-Thinking Exp models.
*   **Image Understanding**: Analyze and research based on visual inputs.
*   **AI Suite**: Integrated tools for sentiment analysis, website summarization, and product comparison.

---

## 🛠️ Technology Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **AI Models** | Google Gemini 2.0 (Flash/Thinking), Groq API (Llama 3) |
| **Data Layer** | SQLModel (SQLAlchemy + Pydantic), SQLite / PostgreSQL |
| **Scraping** | BeautifulSoup4, Requests, Parallel ThreadPoolExecutor |
| **Auth** | JWT (python-jose), Argon2id Hashing |
| **Deployment** | Render, Docker (Optional) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- API Keys for Google Gemini (AI Studio) and Groq

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/veerendra17788/DeepDive_AI.git
   cd DeepDive_AI
   ```

2. **Setup virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_key
   GROQ_API_KEY=your_groq_key
   SECRET_KEY=your_random_jwt_secret
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```
   Visit `http://127.0.0.1:8000` to start exploring!

---

## 🏗️ Architecture Overview

The system utilizes a modular **FastAPI Router** architecture:
- `routers/auth.py`: Secure user registration and JWT management.
- `routers/chat.py`: Real-time AI conversation handling.
- `routers/research.py`: The core iterative scraping and synthesis engine.
- `routers/tools.py`: Specialized AI utilities and job search endpoints.

---

## 📜 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🤝 Founder
Developed with ❤️ by **K. Veerendra Kumar**  
[GitHub Profile](https://github.com/veerendra17788)

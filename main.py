from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database import init_db
from routers import auth
import uvicorn
import os

app = FastAPI(title="Deep Research AI")

# Mount Static (ensure directory exists first)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include Routers
app.include_router(auth.router)
from routers import chat
app.include_router(chat.router)
from routers import research
app.include_router(research.router)
from routers import tools
app.include_router(tools.router)
from routers import settings
app.include_router(settings.router)

@app.get("/research", include_in_schema=False)
async def research_page(request: Request):
    return templates.TemplateResponse("research.html", {"request": request, "active_page": "research"})

@app.get("/jobs", include_in_schema=False)
async def jobs_page(request: Request):
    return templates.TemplateResponse("jobs.html", {"request": request, "active_page": "jobs"})

@app.get("/tools", include_in_schema=False)
async def tools_page(request: Request):
    return templates.TemplateResponse("tools.html", {"request": request, "active_page": "tools"})

@app.get("/settings", include_in_schema=False)
async def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request, "active_page": "settings"})

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
async def root(request: Request):
    # Serve promotional landing page
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "active_page": "chat"})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

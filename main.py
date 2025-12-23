from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from database import init_db
from routers import auth, chat, research, tools, settings

app = FastAPI(title="Deep Research AI")

# Mount Static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include Routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(research.router)
app.include_router(tools.router)
app.include_router(settings.router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
async def root(request: Request):
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

@app.get("/research")
async def research_page(request: Request):
    return templates.TemplateResponse("research.html", {"request": request, "active_page": "research"})

@app.get("/jobs")
async def jobs_page(request: Request):
    return templates.TemplateResponse("jobs.html", {"request": request, "active_page": "jobs"})

@app.get("/tools")
async def tools_page(request: Request):
    return templates.TemplateResponse("tools.html", {"request": request, "active_page": "tools"})

@app.get("/settings")
async def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request, "active_page": "settings"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

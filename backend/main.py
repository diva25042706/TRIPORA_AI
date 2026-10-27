from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import init_db, SessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.api.v1.routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables
    init_db()
    
    # Ensure default demo user exists
    db = SessionLocal()
    try:
        demo_user = db.query(User).filter(User.email == "demo@tripora.ai").first()
        if not demo_user:
            demo_user = User(
                email="demo@tripora.ai",
                hashed_password=hash_password("tripora123"),
                full_name="Alex Vance",
                preferred_currency="INR"
            )
            db.add(demo_user)
            db.commit()
        elif "(Demo Traveller)" in (demo_user.full_name or ""):
            demo_user.full_name = "Alex Vance"
            db.commit()
    finally:
        db.close()
        
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Agentic AI Travel Planner — Multi-Agent Intelligent Trip Planning and Real-Time Travel Assistant",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API Engine",
        "documentation": "/docs",
        "api_v1": "/api/v1",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

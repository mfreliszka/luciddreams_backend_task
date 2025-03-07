"""Module containing app initialization settings."""
from fastapi import FastAPI
from app.routes import auth, posts
from app.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI MVC Example",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

@app.get("/")
def home():
    return {"message": "FastAPI MVC App is running!"}

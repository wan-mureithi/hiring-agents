# src/hiring_agents/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as api_router  # assuming routes.py is in the root

app = FastAPI(
    title="Hiring Automation API",
    description="Talent acquisition backend using LLMs + Airtable",
    version="0.1.0",
)

# (Optional for dev) allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def health_check():
    return {"status": "🚀 API is live"}

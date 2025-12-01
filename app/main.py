from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- NEW IMPORT
from app.api.routes import router

app = FastAPI(
    title="EcoCredit Enterprise API",
    description="AI-Powered Carbon Risk Engine for Fintech",
    version="1.0.0"
)

# NEW: Allow React to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "operational", "system": "EcoCredit Core"}
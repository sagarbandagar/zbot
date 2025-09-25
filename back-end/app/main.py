import os
import sys
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv # type: ignore
from fastapi import FastAPI   # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from routes.chat import router as chat_router
from app.ws_handler import register_ws

# Load environment variables
load_dotenv()

app = FastAPI(title="zbot")

cors_origins = os.getenv("CORS_ORIGINS", "*")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins.split(",") if cors_origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api")

# Register WebSocket
register_ws(app)

@app.get("/")
async def root():
    return {"message": "ZBot API is running"}

if __name__ == "__main__":
    import uvicorn # type: ignore
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
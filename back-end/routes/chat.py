from fastapi import APIRouter, HTTPException # type: ignore
from app.models import ChatRequest
from services.openai_services import chat_completion_with_fallback

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # First try the fallback version which handles quota errors gracefully
        response = chat_completion_with_fallback(request.message)
        return {"response": response}
    except Exception as e:
        # For other errors (connection issues, authentication, etc.), return HTTP error
        error_msg = str(e)
        if "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
            # This shouldn't happen with fallback, but just in case
            return {"response": "I'm currently experiencing service limitations. Please try again later."}
        else:
            raise HTTPException(status_code=500, detail=error_msg)
    
    
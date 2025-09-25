from pydantic import BaseModel # type: ignore

class ChatRequest(BaseModel):
    message: str
import asyncio
import threading
from fastapi import WebSocket # type: ignore
from services import openai_services


def register_ws(app):
    @app.websocket("/ws")
    async def websocket_endpoint(websocket:WebSocket):
        await websocket.accept()
        loop = asyncio.get_event_loop()
        try:
            while True:
                msg = await websocket.receive_text()
                def worker(user_msg:str):
                    try:
                        # Stream response from OpenAI
                        for chunk in openai_services.stream_chat_completion(user_msg):
                            # If chunk contains error messages, clean them up
                            if chunk.startswith("[ERROR]") or "<!DOCTYPE html>" in chunk or len(chunk) > 500:
                                # Extract simple error message
                                if "520" in chunk or "502" in chunk or "503" in chunk:
                                    asyncio.run_coroutine_threadsafe(websocket.send_text("OpenAI is down"),loop)
                                elif "quota" in chunk.lower() or "billing" in chunk.lower():
                                    asyncio.run_coroutine_threadsafe(websocket.send_text("Quota limit reached"),loop)
                                elif "rate limit" in chunk.lower():
                                    asyncio.run_coroutine_threadsafe(websocket.send_text("Rate limit reached"),loop)
                                else:
                                    asyncio.run_coroutine_threadsafe(websocket.send_text("Service unavailable"),loop)
                                break  # Stop streaming if there's an error
                            else:
                                # Normal response chunk
                                asyncio.run_coroutine_threadsafe(websocket.send_text(chunk),loop)
                    except Exception:
                        # Final fallback for any unexpected errors
                        asyncio.run_coroutine_threadsafe(websocket.send_text("Service unavailable"),loop)
                t = threading.Thread(target=worker, args=(msg,),daemon=True)
                t.start()
        except Exception:
            try:
                await websocket.close()
            except Exception:
                pass

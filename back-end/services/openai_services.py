import os
import ssl
import httpx
from dotenv import load_dotenv # type: ignore
from openai import OpenAI # type: ignore
from openai import RateLimitError, APIError, AuthenticationError # type: ignore

# Load environment variables
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")

# Configure SSL context for environments with certificate issues
ssl_context = ssl.create_default_context()
# For corporate environments, you might need to disable SSL verification
# Uncomment the next line if you're in a corporate environment with SSL issues
# ssl_context.check_hostname = False
# ssl_context.verify_mode = ssl.CERT_NONE

# Check if SSL verification should be disabled (for testing/corporate environments)
disable_ssl_verify = os.getenv("DISABLE_SSL_VERIFY", "false").lower() == "true"

# Create HTTP client with timeout and SSL configuration
if disable_ssl_verify:
    print("WARNING: SSL verification is disabled. This is less secure and should only be used for testing.")
    http_client = httpx.Client(
        timeout=30.0,  # 30 second timeout
        verify=False  # Disable SSL verification
    )
else:
    http_client = httpx.Client(
        timeout=30.0,  # 30 second timeout
        verify=ssl_context
    )

client = OpenAI(
    api_key=OPENAI_KEY,
    http_client=http_client
)
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

def chat_completion_sync(message: str, model: str = DEFAULT_MODEL) -> str:
    """Synchronous chat completion"""
    try:
        max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except RateLimitError as e:
        if "insufficient_quota" in str(e).lower():
            raise Exception("quota_exceeded: OpenAI API quota exceeded. Please check your OpenAI account billing and usage limits at https://platform.openai.com/usage")
        else:
            raise Exception(f"rate_limit: OpenAI API rate limit exceeded: {str(e)}. Please wait and try again later.")
    except AuthenticationError as e:
        raise Exception(f"OpenAI API authentication failed: {str(e)}. Please check your API key.")
    except APIError as e:
        raise Exception(f"OpenAI API error: {str(e)}")
    except ssl.SSLError as e:
        raise Exception(f"SSL/Certificate error: {str(e)}. This might be due to corporate firewall or network restrictions.")
    except httpx.ConnectTimeout as e:
        raise Exception(f"Connection timeout: {str(e)}. The OpenAI API might be unreachable.")
    except httpx.ConnectError as e:
        if "certificate verify failed" in str(e).lower():
            raise Exception(f"SSL Certificate verification failed: {str(e)}. This is often caused by corporate firewalls or proxy servers. Please check your network settings.")
        else:
            raise Exception(f"Network connection error: {str(e)}. Unable to reach OpenAI API servers.")
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        
        # Check for quota errors that might be wrapped in other exceptions
        if "insufficient_quota" in error_msg.lower() or "quota" in error_msg.lower():
            raise Exception(f"OpenAI API quota exceeded: {error_msg}")
        else:
            raise Exception(f"OpenAI API error ({error_type}): {error_msg}")

def get_fallback_response(message: str) -> str:
    """Provide a fallback response when OpenAI API is unavailable"""
    fallback_responses = {
        "hello": "Hello! I'm ZBot, but I'm currently running on limited mode because the OpenAI API quota has been exceeded. Please check your OpenAI billing at https://platform.openai.com/usage",
        "help": "I'd love to help, but I'm currently unable to access the AI service due to quota limitations. Please add billing details to your OpenAI account or wait for quota reset.",
        "test": "🚨 Service Status: OpenAI API quota exceeded. Please check your OpenAI account billing and usage limits at https://platform.openai.com/usage",
        "default": f"I received your message: '{message[:50]}{'...' if len(message) > 50 else ''}' but I'm currently in limited mode due to OpenAI API quota being exceeded. Please check your billing at https://platform.openai.com/usage"
    }
    
    message_lower = message.lower().strip()
    for key, response in fallback_responses.items():
        if key in message_lower:
            return response
    
    return fallback_responses["default"]

def chat_completion_with_fallback(message: str, model: str = DEFAULT_MODEL) -> str:
    """Chat completion with fallback response"""
    try:
        return chat_completion_sync(message, model)
    except Exception as e:
        # Log the error for debugging
        print(f"OpenAI API Error: {e}")
        
        # Check if it's a quota error and provide fallback
        if "quota_exceeded" in str(e) or "rate_limit" in str(e) or "quota" in str(e).lower() or "insufficient_quota" in str(e).lower():
            return get_fallback_response(message)
        else:
            # For other errors, still raise the exception with more specific info
            raise Exception(f"OpenAI API error: {str(e)}")

def stream_chat_completion(message: str, model: str = DEFAULT_MODEL):
    """Streaming chat completion"""
    try:
        max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        # Super simple error handling - just basic messages
        error_msg = str(e).lower()
        
        # Check for specific issues and return ONE simple word/phrase
        if "520" in error_msg or "502" in error_msg or "503" in error_msg or "<!doctype" in error_msg:
            yield "OpenAI is down"
        elif "quota" in error_msg or "billing" in error_msg or "insufficient" in error_msg:
            yield "Quota limit reached"
        elif "rate limit" in error_msg or "429" in error_msg:
            yield "Rate limit reached"
        elif "401" in error_msg or "unauthorized" in error_msg or "api key" in error_msg:
            yield "API key invalid"
        else:
            yield "Service unavailable"
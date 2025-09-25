"""
Multi-provider AI service that supports OpenAI, Ollama, and other free alternatives
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MultiProviderAIService:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "openai").lower()
        self.service = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize the appropriate AI service based on provider"""
        if self.provider == "openai":
            try:
                from .openai_services import OpenAIService
                self.service = OpenAIService()
            except ImportError as e:
                print(f"OpenAI service not available: {e}")
                self._fallback_to_free_service()
        
        elif self.provider == "ollama":
            try:
                from .ollama_service import OllamaService
                self.service = OllamaService()
                if not self.service.check_status():
                    print("Ollama server not running. Please start with: ollama serve")
                    self._fallback_to_free_service()
            except ImportError as e:
                print(f"Ollama service not available: {e}")
                self._fallback_to_free_service()
        
        elif self.provider == "huggingface":
            try:
                from .huggingface_service import HuggingFaceService
                self.service = HuggingFaceService()
            except ImportError as e:
                print(f"HuggingFace service not available: {e}")
                self._fallback_to_free_service()
        
        else:
            print(f"Unknown provider: {self.provider}. Falling back to mock service.")
            self._fallback_to_free_service()
    
    def _fallback_to_free_service(self):
        """Fallback to a mock service for testing"""
        self.service = MockAIService()
        print("Using mock AI service for testing. Set AI_PROVIDER environment variable.")
    
    def get_chat_response(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Get response from the configured AI provider"""
        try:
            if hasattr(self.service, 'get_chat_response'):
                return self.service.get_chat_response(message, system_prompt)
            elif hasattr(self.service, 'generate_response'):
                prompt = f"{system_prompt}\n\nUser: {message}" if system_prompt else message
                return self.service.generate_response(prompt)
            else:
                return self.service.get_response(message)
        except Exception as e:
            return f"Error getting AI response: {str(e)}"
    
    def get_provider_info(self) -> dict:
        """Get information about the current provider"""
        status = "unknown"
        if hasattr(self.service, 'check_status'):
            status = "online" if self.service.check_status() else "offline"
        
        return {
            "provider": self.provider,
            "status": status,
            "service_type": type(self.service).__name__
        }

class MockAIService:
    """Mock AI service for testing when no real provider is available"""
    
    def get_response(self, message: str) -> str:
        """Return a mock response"""
        responses = [
            f"I understand you're asking about: '{message}'. This is a mock response for testing.",
            f"Thanks for your message: '{message}'. I'm a test AI assistant.",
            f"You said: '{message}'. I'm currently in testing mode.",
            f"Regarding '{message}' - I'm a mock AI service. Please configure a real AI provider."
        ]
        # Simple hash-based selection for consistent responses
        index = hash(message) % len(responses)
        return responses[index]
    
    def get_chat_response(self, message: str, system_prompt: str = None) -> str:
        """Return a mock chat response"""
        if system_prompt:
            return f"[Mock AI with system: {system_prompt[:50]}...] Response to: {message}"
        return self.get_response(message)
    
    def check_status(self) -> bool:
        """Mock service is always available"""
        return True

# Create a global instance
ai_service = MultiProviderAIService()
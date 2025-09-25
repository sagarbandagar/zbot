"""
Hugging Face Transformers service for free LLM inference
Completely free alternative using local inference
"""
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class HuggingFaceService:
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers library not installed. Run: pip install transformers torch")
        
        self.model_name = model_name
        self.generator = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Load the model for inference"""
        try:
            if "DialoGPT" in self.model_name:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                self.tokenizer.pad_token = self.tokenizer.eos_token
            else:
                self.generator = pipeline(
                    "text-generation",
                    model=self.model_name,
                    device=0 if self.device == "cuda" else -1
                )
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def generate_response(self, prompt: str, max_length: int = 100) -> str:
        """Generate response using Hugging Face model"""
        try:
            if not self.generator and not self.model:
                if not self.load_model():
                    return "Error: Could not load model"
            
            if "DialoGPT" in self.model_name:
                # For conversational models
                inputs = self.tokenizer.encode(prompt + self.tokenizer.eos_token, return_tensors="pt")
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        inputs,
                        max_length=inputs.shape[1] + max_length,
                        pad_token_id=self.tokenizer.eos_token_id,
                        temperature=0.7,
                        do_sample=True
                    )
                
                response = self.tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
                return response.strip()
            else:
                # For general text generation
                result = self.generator(prompt, max_length=max_length, num_return_sequences=1)
                return result[0]['generated_text'].replace(prompt, '').strip()
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def check_status(self) -> bool:
        """Check if the service is ready"""
        return TRANSFORMERS_AVAILABLE
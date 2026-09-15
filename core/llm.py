import torch
from tokenizers import Tokenizer
import os
import requests
import json

class LlmEngine:
    """Core brain: Hybrid Local PyTorch Transformer + Optional Cloud API via Groq/OpenAI."""
    
    def __init__(self, use_online=False, api_key=""):
        self.device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        self.use_online = use_online
        self.api_key = api_key
        
        # Load the custom tokenizer
        tokenizer_path = os.path.join("training", "jarvis_tokenizer.json")
        try:
            self.tokenizer = Tokenizer.from_file(tokenizer_path)
            self.vocab_size = self.tokenizer.get_vocab_size()
        except:
            print("Warning: Tokenizer not found. Did you run the training script?")
            self.tokenizer = None
            
        # Lazy load the model architecture to prevent circular imports on boot if not trained
        try:
            from models.transformer import JarvisGPT
            self.model = JarvisGPT(
                vocab_size=self.vocab_size,
                n_embd=64,
                n_head=4,
                n_layer=4,
                block_size=32,
                dropout=0.0
            )
            # Load weights
            weights_path = os.path.join("checkpoints", "jarvis_gpt_v1.pth")
            self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            
            if self.use_online:
                print("[✓] JARVIS Neural Brain Loaded (HYBRID MODE: Local + Cloud Activated).")
            else:
                print("[✓] JARVIS Neural Brain Loaded Successfully (Offline Mode).")
        except Exception as e:
            print(f"Warning: Model could not be loaded. Please train first. Error: {e}")
            self.model = None
            
    def _fetch_from_cloud(self, text):
        """Used for answering complex internet questions via Groq API (super fast)."""
        if not self.api_key:
            return "I am unable to reach the cloud. My API key is missing."
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",  # Updated to the latest active Groq Llama model
            "messages": [
                {"role": "system", "content": "You are JARVIS, an intelligent AI assistant. Keep all answers extremely concise, under 2 sentences. You do not need to introduce yourself unless explicitly asked."},
                {"role": "user", "content": text}
            ]
        }
        
        try:
            print(f"   [JARVIS Brain] Thinking... (Cloud: Groq Llama 3.1)")
            # We use Groq because it is extremely fast and matches the 'Jarvis' feeling better than OpenAI delays
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                error_msg = response.json().get('error', {}).get('message', 'Unknown Error')
                return f"Cloud connection failed {response.status_code}: {error_msg}"
        except Exception as e:
            return "Sir, I am having trouble connecting to the cloud servers right now."

    def generate_response(self, text):
        """Routing Architecture: Decide whether to use Local Automations or Cloud Brain."""
        # 1. First, check if the LLM thinks it's a general knowledge/internet query!
        trigger_phrases = ["what is", "who is", "how do", "tell me", "explain", "who was", "search", "joke"]
        clean_text = text.lower().strip()
        
        # Exceptions that SHOULD be local
        local_exceptions = ["what is my heart rate", "what is the time", "what is the date", "what is my battery", "who are you"]
        
        is_cloud_query = any(phrase in clean_text for phrase in trigger_phrases) and not any(exc in clean_text for exc in local_exceptions)
        
        if is_cloud_query and self.use_online:
            return self._fetch_from_cloud(text)
            
        # 2. RUN LOCAL OFFLINE MODEL INFERENCE
        formatted_text = clean_text.capitalize()
        
        if not self.model or not self.tokenizer:
            if "who are you" in formatted_text.lower():
                return "I am JARVIS-OS, a locally intelligent multimodal assistant for personal automation."
            return "My neural network is currently offline. Please run the training script."
            
        input_ids = self.tokenizer.encode(formatted_text).ids
        context = torch.tensor(input_ids, dtype=torch.long, device=self.device).unsqueeze(0)
        
        with torch.no_grad():
            generated_ids = self.model.generate(context, max_new_tokens=15)[0].tolist()
            
        new_tokens = generated_ids[len(input_ids):]
        response = self.tokenizer.decode(new_tokens)
            
        response = response.replace("[EOS]", "").strip()
        response = response.replace(" .", ".").replace(" ,", ",").replace(" ?", "?").replace(" !", "!")
        
        # 3. Final Fallback: If local model hallucinates, and online mode is ON, route to Cloud!
        if "I am a local system automation AI" in response and self.use_online:
            return self._fetch_from_cloud(text)
            
        return response

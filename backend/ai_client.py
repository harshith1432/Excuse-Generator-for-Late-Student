import os
from huggingface_hub import InferenceClient

class AIClient:
    def __init__(self):
        self.api_key = os.environ.get('HUGGINGFACE_API_KEY')
        self.client = InferenceClient(
            model="Qwen/Qwen2.5-7B-Instruct",
            token=self.api_key
        )

    def generate_text(self, prompt, max_new_tokens=500, temperature=0.7):
        if not self.api_key:
            return "Error: HUGGINGFACE_API_KEY not found in environment variables."

        try:
            # Using chat-like format for instruction models
            response = self.client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_new_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI Client Error: {e}")
            return f"Error interacting with AI: {str(e)}"

# Create a singleton instance
ai_client = AIClient()

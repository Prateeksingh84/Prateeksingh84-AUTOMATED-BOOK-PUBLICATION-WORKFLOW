# src/llm_client.py

import google.generativeai as genai
import os

class LLMService:
    """
    Manages interaction with the Google Generative AI models.
    API key is loaded from the GEMINI_API_KEY environment variable.
    """
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        api_key = os.getenv("AIzaSyCSnOOVhagR4keZv5Qt3q9U680d8gCLzRs")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please set your Gemini API key.")
        
        genai.configure(api_key=api_key) 
        self.model = genai.GenerativeModel(model_name)
        print(f"Initialized LLMService with model: {model_name}")

    def generate_content(self, prompt: str) -> str:
        """
        Sends a prompt to the configured LLM and returns the generated text.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content with LLM: {e}")
            return f"Error: Could not generate content. {e}"


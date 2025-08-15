import google.generativeai as genai
import os

class LLMService:
    """Manages interaction with the Google Generative AI model."""
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        # CORRECTED LINE: Retrieve the API key using the variable's NAME
        api_key = os.getenv("GEMINI_API_KEY") # <--- THIS IS THE FIX
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set. Please ensure it's set correctly.")
            
        genai.configure(api_key=api_key) 
        self.model = genai.GenerativeModel(model_name)

    def generate_content(self, prompt: str) -> str:
        """Sends a prompt to the model and returns the text response."""
        response = self.model.generate_content(prompt)
        return response.text

class AIWriter:
    """Uses an LLM to perform creative writing tasks."""
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def rewrite_chapter(self, original_text: str) -> str:
        """Rewrites a chapter with a creative prompt."""
        prompt = (
            f"You are a creative writer. Rewrite the following chapter to make it more engaging "
            f"and descriptive, with a focus on character emotions and setting. "
            f"Original chapter text:\n\n{original_text}"
        )
        return self.llm.generate_content(prompt)

if __name__ == "__main__":
    try:
        llm_service = LLMService()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your GEMINI_API_KEY environment variable as instructed.")
        exit()

    ai_writer = AIWriter(llm_service)

    sample_chapter = """
    John walked through the forest. It was a cold day. He saw a bird in a tree. The bird was blue. 
    He felt a little sad because he was all alone.
    """

    rewritten_text = ai_writer.rewrite_chapter(sample_chapter)
    print("--- Original Chapter ---")
    print(sample_chapter)
    print("\n--- Rewritten Chapter ---")
    print(rewritten_text)
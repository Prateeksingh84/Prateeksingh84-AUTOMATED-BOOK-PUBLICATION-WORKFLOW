import google.generativeai as genai
import os

class LLMService:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        # Correctly get the API key from an environment variable.
        # You must set this environment variable first.
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
            
        genai.configure(api_key=api_key) 
        self.model = genai.GenerativeModel(model_name)

    def generate_content(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text

class AIReviewer:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def review_rewrite(self, original_text: str, rewritten_text: str) -> str:
        """Compares the original and rewritten chapters and provides feedback."""
        prompt = (
            f"You are an expert editor. Review the rewritten chapter below and provide feedback "
            f"on its coherence, style, and how well it aligns with the original text. "
            f"Point out specific areas for improvement. "
            f"Original:\n\n{original_text}\n\n"
            f"Rewritten:\n\n{rewritten_text}"
        )
        return self.llm.generate_content(prompt)

if __name__ == "__main__":
    # --- Example Usage ---
    try:
        llm_service = LLMService()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your GEMINI_API_KEY environment variable.")
        exit()

    ai_reviewer = AIReviewer(llm_service)

    original_text = "John walked through the forest. It was a cold day. He saw a blue bird in a tree. He felt a little sad."
    rewritten_text = "With a heavy heart, John journeyed into the hushed, cold forest. The air bit at his cheeks, and a stark, cobalt-winged bird watched him from a high branch, mirroring the deep solitude he felt."

    review_output = ai_reviewer.review_rewrite(original_text, rewritten_text)
    print("--- Review of Rewritten Chapter ---")
    print(review_output)
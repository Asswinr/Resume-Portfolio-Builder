import os
import google.generativeai as genai

def initialize_gemini():
    """Initializes the Gemini API client using the GEMINI_API_KEY environment variable."""
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.5-pro')
    except Exception as e:
        print(f"Error initializing Gemini API: {e}")
        return None

def generate_ai_content(prompt: str) -> str:
    """
    Generates content using the Gemini AI model.

    Args:
        prompt: The text prompt to send to the AI.

    Returns:
        The generated text content from the AI, or an error message if something goes wrong.
    """
    model = initialize_gemini()
    if not model:
        return "Error: Gemini API not initialized."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating AI content: {e}"

if __name__ == '__main__':
    # Example usage (this will only run if you execute ai_utils.py directly)
    test_prompt = "Write a short, catchy headline for a resume builder."
    print(f"Generating content for prompt: '{test_prompt}'")
    generated_text = generate_ai_content(test_prompt)
    print("\nGenerated AI Content:")
    print(generated_text)
from google import genai
import os

MODEL = "gemini-2.5-flash"

def main():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL,
        contents=(
            "You are RufusAI, an AI assistant. Please provide helpful OIT support information by "
            "scraping Ohio University help.ohio.edu articles. Respond in a friendly and professional "
            "manner. Keep responses short while still being informative.\n\n"
            "User: How do I log on to the school Wi-Fi?\n"
            "RufusAI:"
        ),
    )
    print(response.text)

if __name__ == "__main__":
    main()
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

    response2 = client.models.generate_content(
        model=MODEL,
        contents=(
            "You are RufusAI, an AI assistant. Please provide helpful OIT support information by "
            "scraping Ohio University help.ohio.edu articles. Respond in a friendly and professional "
            "manner. Keep responses short while still being informative.\n\n"
            "User: How do I reset my Ohio University password?\n"
            "RufusAI:"
        ),
    )
    print("\n --- \n")
    print(response2.text)

    response3 = client.models.generate_content(
        model=MODEL,
        contents=(
            "You are RufusAI, an AI assistant. Please provide helpful OIT support information by "
            "scraping Ohio University help.ohio.edu articles. Respond in a friendly and professional "
            "manner. Keep responses short while still being informative.\n\n"
            "User: What does my Ohio University email address look like?\n"
            "RufusAI:"
        ),
    )
    print("\n --- \n")
    print(response3.text)


if __name__ == "__main__":
    main()

# Acceptance Criteria:
# - The script uses the Gemini API to generate responses.
# - It gets the API key from an environment variable.
# - The script handles the case where the API key is not set.
# - It generates three different responses based on user queries about Ohio University IT support.
# - The responses are printed to the console.
# - Accuracy is ≥ 50% 
import asyncio
import io
from pathlib import Path
import wave
from google import genai
from google.genai import types
import soundfile as sf
import librosa
import os

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("Please set the GEMINI_API_KEY environment variable")
client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash-native-audio-preview-09-2025"


config = {
  "response_modalities": ["AUDIO"],
  "system_instruction": "You are RufusAI, an AI assistant. Please provide helpful OIT support information by "
            "scraping Ohio University help.ohio.edu articles. Respond in a friendly and professional "
            "manner. Keep responses short while still being informative.\n\n",
}

async def main():
    async with client.aio.live.connect(model=MODEL, config=config) as session:
        buffer = io.BytesIO()
        y, sr = librosa.load("sample.wav", sr=16000)
        sf.write(buffer, y, sr, format='RAW', subtype='PCM_16')
        buffer.seek(0)
        audio_bytes = buffer.read()


        await session.send_realtime_input(
            audio=types.Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")
        )

        wf = wave.open("audio.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)

        async for response in session.receive():
            if response.data is not None:
                wf.writeframes(response.data)

            # Un-comment this code to print audio data info
            # if response.server_content.model_turn is not None:
            #      print(response.server_content.model_turn.parts[0].inline_data.mime_type)

        wf.close()

    # api_key = os.getenv('GEMINI_API_KEY')
    # if not api_key:
    #     raise ValueError("Please set the GEMINI_API_KEY environment variable")
    # client = genai.Client(api_key=api_key)
    # response = client.models.generate_content(
    #     model=MODEL,
    #     contents=(
    #         "You are RufusAI, an AI assistant. Please provide helpful OIT support information by "
    #         "scraping Ohio University help.ohio.edu articles. Respond in a friendly and professional "
    #         "manner. Keep responses short while still being informative.\n\n"
    #         "User: How do I log on to the school Wi-Fi?\n"
    #         "RufusAI:"
    #     ),
    # )
    # print(response.text)

    # response2 = client.models.generate_content(
    #     model=MODEL,
    #     contents=(
    #         "You are RufusAI, an AI assistant. Please provide helpful OIT support information by "
    #         "scraping Ohio University help.ohio.edu articles. Respond in a friendly and professional "
    #         "manner. Keep responses short while still being informative.\n\n"
    #         "User: How do I reset my Ohio University password?\n"
    #         "RufusAI:"
    #     ),
    # )
    # print("\n --- \n")
    # print(response2.text)

    # response3 = client.models.generate_content(
    #     model=MODEL,
    #     contents=(
    #         "You are RufusAI, an AI assistant. Please provide helpful OIT support information by "
    #         "scraping Ohio University help.ohio.edu articles. Respond in a friendly and professional "
    #         "manner. Keep responses short while still being informative.\n\n"
    #         "User: What does my Ohio University email address look like?\n"
    #         "RufusAI:"
    #     ),
    # )
    # print("\n --- \n")
    # print(response3.text)


if __name__ == "__main__":
    asyncio.run(main())

# Acceptance Criteria:
# - The script uses the Gemini API to generate responses.
# - It gets the API key from an environment variable.
# - The script handles the case where the API key is not set.
# - It generates three different responses based on user queries about Ohio University IT support.
# - The responses are printed to the console.
# - Accuracy is ≥ 50% 
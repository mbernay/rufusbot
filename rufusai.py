import asyncio
import io
import queue
import threading
import wave
from google import genai
from google.genai import types
import soundfile as sf
import os
import pyaudio
import keyboard
import numpy as np

# Set your API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("Please set the GEMINI_API_KEY environment variable")

client = genai.Client(api_key=api_key)

# Audio configuration
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1

# Model configuration
MODEL = "gemini-2.5-flash-native-audio-preview-09-2025"

config = {
    "response_modalities": ["AUDIO"],
    "system_instruction": "You are RufusAI, an AI assistant. Please provide helpful OIT support information by "
            "scraping Ohio University help.ohio.edu articles. Respond in a friendly and professional "
            "manner. Keep responses short while still being informative.\n\n",
}

class AudioIO:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.recording_thread = None
        
    def start_recording(self):
        # Start recording audio from microphone
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        
    def stop_recording(self):
        # Stop recording audio
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join()
            
    def _record_audio(self):
        # Record audio in a separate thread
        stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)
        #print("Recording... Release SPACE to stop and send")
        while self.is_recording:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                self.audio_queue.put(data)
        stream.stop_stream()
        stream.close()
            
    def get_recorded_audio(self):
        # Get all recorded audio data
        audio_data = b''
        while not self.audio_queue.empty():
            audio_data += self.audio_queue.get()
        return audio_data
        
    def play_audio(self, audio_data, sample_rate=24000):
        # Play audio through speakers
        stream = self.audio.open(format=FORMAT, channels=CHANNELS,rate=sample_rate, output=True)
        stream.write(audio_data)
        stream.stop_stream()
        stream.close()
            
    def cleanup(self):
        # Clean up audio resources
        self.stop_recording()
        self.audio.terminate()

async def main():
    # Main conversation loop
    streamer = AudioIO()
    async with client.aio.live.connect(model=MODEL, config=config) as session:
        print("Type your questions to get audio responses")
        
        while True:
            print("\nYour question:")
            user_text = input("> ").strip()
            
            if not user_text:
                print("No question entered")
                continue
            
            if user_text.lower() == 'q':
                break
            
            
            # Send text to Live API
            await session.send_realtime_input(text=user_text)
            
            
            # Collect response audio
            response_audio = b''
            max_wait_time = 20
            
            try:
                async def collect_response():
                    collected_audio = b''
                    last_data_time = asyncio.get_event_loop().time()
                    async for response in session.receive():
                        current_time = asyncio.get_event_loop().time()

                        if response.data is not None:
                            collected_audio += response.data
                            last_data_time = current_time
                            # Print dots to indicate receiving audio chunks to track progress
                            print(".", end="", flush=True)
                        
                        # Stop if no data for 1.5 seconds and we have audio
                        if (current_time - last_data_time) > 1.5 and len(collected_audio) > 0:
                            break
                    
                    return collected_audio
                
                response_audio = await asyncio.wait_for(collect_response(), timeout=max_wait_time)
                print()
            except asyncio.TimeoutError:
                print("\nResponse timed out")
            
            # Play response
            if response_audio:
                streamer.play_audio(response_audio)
            else:
                print("No response received")
            
            print("\n(Press SPACE for another question, or Q to quit)")
            if keyboard.is_pressed('q'):
                break
    streamer.cleanup()

if __name__ == "__main__":
    print("Starting RufusAI Live Chat")
    #print("Make sure microphone and speakers are working")

    asyncio.run(main())
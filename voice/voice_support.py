# src/voice/voice_support.py

import speech_recognition as sr
from gtts import gTTS
import os
import asyncio # Required for async operations like sleep
import pyglet # Using pyglet for audio playback
import time # Explicitly import time for time.sleep

# IMPORTANT: This file defines the functions. It DOES NOT need to import them from itself.
# The problematic line 'from voice.voice_support import ...' HAS BEEN REMOVED.

def list_microphones():
    """Lists all available microphones and their indices."""
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone with index {index}: {name}")
    print("-" * 30)

def listen_for_input(device_index=None):
    """
    Listens for user voice input from a specified microphone device and returns the recognized text.
    Uses Google Web Speech API for recognition.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone(device_index=device_index) as source:
            print("Listening for voice input...")
            # Adjust for ambient noise for better recognition
            recognizer.adjust_for_ambient_noise(source) 
            # Increased timeout to 8 seconds to give more time for user input
            audio = recognizer.listen(source, timeout=8) 
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return ""
    except sr.WaitTimeoutError:
        print("No audio received within timeout period.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; check your internet connection or API limits: {e}")
        return ""
    except Exception as e: # Catch other potential microphone/audio errors
        print(f"An error occurred with the microphone: {e}")
        return ""

def speak_text(text: str, lang: str = 'en'):
    """
    Converts text to speech using Google Text-to-Speech (gTTS) and plays it
    using pyglet. Saves a temporary MP3 file and then removes it.
    """
    try:
        if not text:
            print("No text to speak.")
            return

        tts = gTTS(text=text, lang=lang, slow=False)
        temp_audio_file = "response.mp3"
        tts.save(temp_audio_file)
        
        print(f"Speaking: '{text}'")
        
        # Load the audio file using pyglet
        # streaming=False means the entire file is loaded into memory, good for short clips
        music = pyglet.media.load(temp_audio_file, streaming=False)
        
        # Create a player instance
        player = pyglet.media.Player()
        
        # Queue the music to the player
        player.queue(music)
        
        # Play the audio
        player.play()

        # pyglet requires an event loop to play audio. 
        # For simple, blocking playback without a full GUI, a short sleep is often sufficient 
        # for the audio to start playing, and then we wait for playback to finish.
        
        # Give pyglet a moment to start playing
        time_to_play = music.duration # Get the duration of the audio
        if time_to_play > 0:
            # Sleep for the duration of the audio plus a small buffer
            time.sleep(time_to_play + 0.5) 
        else:
            # Fallback if duration isn't available or is zero
            time.sleep(2) 
        
        # Ensure the player is stopped and resources are released
        player.pause() 
        player.delete() # Important to release resources

        # Clean up the temporary audio file
        os.remove(temp_audio_file)
        print("Audio playback finished and file deleted.")

    except Exception as e:
        print(f"An error occurred with TTS or audio playback: {e}")

# Example usage (for testing purposes only, this module is usually imported by other files)
if __name__ == "__main__":
    print("Running voice_support.py directly for testing:")
    
    # Call list_microphones directly as it's defined in this module
    list_microphones() 
    
    # You can change this index based on your system's microphone configuration
    mic_index_to_use = None # Set to None to use default, or an integer index
    print(f"Using microphone with index {mic_index_to_use} (or default if None).")

    speak_text("Hello. This is a test from the voice support module using pyglet.")
    
    print("\nAttempting to listen now...")
    user_speech = listen_for_input(device_index=mic_index_to_use)
    if user_speech:
        speak_text(f"You just said: {user_speech}")
    else:
        speak_text("I didn't detect any speech.")
    
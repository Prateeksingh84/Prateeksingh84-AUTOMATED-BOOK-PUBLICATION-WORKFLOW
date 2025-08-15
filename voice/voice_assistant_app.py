# src/voice_assistant_app.py

import asyncio
import os
import datetime
import speech_recognition as sr # Needed for list_microphones
import sys

# Add the 'src' directory to the system path to enable module imports
# This allows importing 'voice.voice_support' and 'scraping.scraper'
current_dir = os.path.dirname(os.path.abspath(__file__))
# Assumes 'voice_assistant_app.py' is in 'src' and other modules are in 'src/voice', 'src/scraping', etc.
project_root = os.path.join(current_dir, '..') 
if project_root not in sys.path:
    sys.path.append(project_root)

# Import functions from the 'voice_support.py' module
from voice.voice_support import listen_for_input, speak_text, list_microphones # Added list_microphones import

# Import the scrape_chapter function from the scraping module
from scraping.scraper import scrape_chapter

# The URL for the chapter to be summarized
CHAPTER_URL = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
DATA_DIR = "data" # Directory where scraped content is saved

def get_chapter_summary(chapter_content: str) -> str:
    """
    A simplified summarization function. In a full workflow, this would
    be replaced by an LLM-based summarization from an AI agent.
    """
    words = chapter_content.split()
    # Return the first 100 words as a basic summary
    summary = " ".join(words[:100]) + "..."
    return summary

async def get_summary_logic():
    """
    Handles the logic for scraping a chapter and providing a summary.
    """
    print(f"Requesting summary for chapter at URL: {CHAPTER_URL}")
    speak_text("I am now getting the summary for the chapter.")
    
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Scrape the chapter content
    # scrape_chapter is an async function, so await its result
    scraped_result = await scrape_chapter(CHAPTER_URL, output_dir=DATA_DIR)

    if scraped_result:
        text_file_path, _ = scraped_result # Unpack the tuple, we only need the text path here
        try:
            with open(text_file_path, "r", encoding="utf-8") as f:
                chapter_content = f.read()
            summary = get_chapter_summary(chapter_content)
            
            print("Here is a summary of the chapter:") # Print text to console
            print(summary)                               # Print summary text
            speak_text("Here is a summary of the chapter.") # This line speaks the intro
            speak_text(summary)                           # <--- THIS LINE SPEAKS THE SUMMARY ITSELF
        except FileNotFoundError:
            speak_text("I was unable to read the scraped content file.")
            print("Error: Scraped content file not found.")
        except Exception as e:
            speak_text(f"An error occurred while processing the summary: {e}")
            print(f"Error processing summary: {e}")
    else:
        speak_text("I was unable to scrape the content from that URL.")
        print("Error: Scraping failed for the chapter URL.")

def get_weather():
    """Provides a mock weather report."""
    speak_text("I can't get the live weather right now, but it looks like a sunny day!")
    print("Mock Weather: Sunny day!")

def tell_time():
    """Tells the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak_text(f"The current time is {current_time}")
    print(f"Current Time: {current_time}")

async def run_voice_assistant():
    """
    Main function to run the voice assistant.
    """
    list_microphones() # Call the imported function
    
    # You can change this index based on your system's microphone configuration
    # Use list_microphones() output to determine the correct index.
    mic_index_to_use = None # Set to None to use default microphone, or an integer index
    print(f"Using microphone with index {mic_index_to_use} (or default if None).")

    print("\nStarting voice assistant.")
    
    speak_text("Hello. I am your voice assistant. Please tell me how I can help you.")
    
    user_input = listen_for_input(device_index=mic_index_to_use)
    
    if user_input:
        command = user_input.lower()
        
        if "weather" in command:
            get_weather()
        elif "time" in command:
            tell_time()
        elif "summary" in command or "summarize" in command or "summarise" in command: # Added 'summarise' for common spelling
            await get_summary_logic() # Call the async function
        else:
            speak_text(f"I don't know how to handle the command: {user_input}. Please try again.")
            print(f"Unknown command: {user_input}")
    else:
        speak_text("I didn't hear anything, please try again.")
        print("No voice input detected.")

if __name__ == "__main__":
    # Run the async voice assistant
    asyncio.run(run_voice_assistant())


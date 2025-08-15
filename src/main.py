# src/main.py

import asyncio
import os
import configparser
import time

from llm_client import LLMService 
from scraping.scraper import scrape_chapter
from agents.writer_agent import AIWriter
from agents.reviewer_agent import AIReviewer
from database.chromadb_manager import (
    initialize_chromadb,
    create_or_get_collection,
    add_chapter_version,
    get_chapter_versions,
)
from voice.voice_support import speak_text, listen_for_input
from scraping.rl_reward import calculate_reward


# --- Configuration Loading ---
config = configparser.ConfigParser()
config_file_path = 'config.ini' 
if os.path.exists(config_file_path):
    config.read(config_file_path)
    DATA_DIR = config.get('Paths', 'data_dir', fallback='data')
    CHROMA_DB_PATH = config.get('Database', 'path', fallback='./chroma_db')
else:
    print(f"Warning: {config_file_path} not found. Using default paths.")
    DATA_DIR = "data"
    CHROMA_DB_PATH = "./chroma_db"

CHAPTER_URL = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"

def get_chapter_summary(chapter_content: str) -> str:
    """
    A simplified summarization function. In a full workflow, this would
    be replaced by an LLM-based summarization from an AI agent.
    """
    words = chapter_content.split()
    summary = " ".join(words[:100]) + "..."
    return summary

async def automated_publication_workflow():
    """
    Orchestrates the entire automated book publication workflow.
    """
    print("🚀 Starting the Automated Book Publication Workflow...")
    speak_text("Starting the automated book publication workflow.")

    os.makedirs(DATA_DIR, exist_ok=True)

    # --- Step 1: Scrape Content ---
    print("\n--- Step 1: Scraping content from the web ---")
    speak_text("Scraping content from the web.")
    
    scraped_result = await scrape_chapter(CHAPTER_URL, output_dir=DATA_DIR)
    
    if not scraped_result:
        print("Error: Scraping failed. Exiting.")
        speak_text("Scraping failed. Exiting workflow.")
        return

    text_file_path, screenshot_path = scraped_result

    original_chapter_text = ""
    try:
        with open(text_file_path, "r", encoding="utf-8") as f:
            original_chapter_text = f.read()
        print("✅ Successfully scraped and read the original chapter text.")
        speak_text("Original chapter content successfully scraped.")
    except FileNotFoundError:
        print("Error: Scraped content file not found. Exiting.")
        speak_text("Scraped content file not found. Exiting workflow.")
        return

    # --- Step 2: Initializing ChromaDB for versioning ---
    print("\n--- Step 2: Initializing ChromaDB for versioning ---")
    speak_text("Initializing the database for chapter versioning.")
    chroma_client = initialize_chromadb(path=CHROMA_DB_PATH)
    chapters_collection = create_or_get_collection(chroma_client, "book_chapters")

    add_chapter_version(chapters_collection, "chapter_1", original_chapter_text, "original", screenshot_path=screenshot_path)
    print("✅ Original chapter version and screenshot path stored in ChromaDB.")
    speak_text("Original chapter version and screenshot stored in the database.")

    # --- Step 3: AI writing and review cycle ---
    print("\n--- Step 3: AI writing and review cycle ---")
    speak_text("Starting AI writing and review process.")
    
    llm_service = LLMService(model_name="gemini-1.5-pro") 
    writer = AIWriter(llm_service)
    reviewer = AIReviewer(llm_service)

    print("AIWriter: Generating new chapter draft...")
    speak_text("AI writer is now generating the first draft.")
    ai_rewrite = writer.rewrite_chapter(original_chapter_text)
    add_chapter_version(chapters_collection, "chapter_1", ai_rewrite, "ai_draft_1")
    print("✅ AI draft 1 created and stored.")
    speak_text("First AI draft created and stored.")
    
    print("\nAIReviewer: Generating review feedback...")
    speak_text("AI reviewer is now analyzing the draft.")
    review_feedback = reviewer.review_rewrite(original_chapter_text, ai_rewrite)
    print(f"\nAI Reviewer Feedback:\n---\n{review_feedback}\n---")
    speak_text("AI review complete. Please check the console for feedback.")

    # --- Step 4: Human-in-the-Loop review ---
    print("\n--- Step 4: Human-in-the-Loop review ---")
    speak_text("Human in the loop review. Please provide your input.")
    print("Presenting original, AI draft, and AI feedback to a human for review...")
    print("You can type 'approve' to accept the AI draft, or type your own edits/feedback.")
    
    speak_text("Please say your edits or 'approve' to finalize.")
    human_input_voice = listen_for_input()
    human_input = human_input_voice if human_input_voice else input("Or type your edits/feedback here: ")

    final_text = ""
    if human_input.lower() == "approve":
        print("Human approved the AI draft.")
        speak_text("Human approved the AI draft.")
        final_text = ai_rewrite
    else:
        final_text = human_input 
        print("Human provided new edits. Storing as the final version.")
        speak_text("Human provided new edits. Storing as the final version.")

    add_chapter_version(chapters_collection, "chapter_1", final_text, "final_draft")
    print("✅ Final chapter version stored in ChromaDB.")
    speak_text("Final chapter version stored in the database.")

    # --- Step 5: Generate and Save Chapter Summary to file and DB ---
    print("\n--- Step 5: Generating and saving chapter summary ---")
    speak_text("Generating a summary of the chapter.")
    chapter_summary = get_chapter_summary(original_chapter_text)
    
    # Save the summary to a text file on disk
    summary_file_path = os.path.join(DATA_DIR, "chapter_1_summary.txt")
    try:
        with open(summary_file_path, "w", encoding="utf-8") as f:
            f.write(chapter_summary)
        print(f"✅ Chapter summary saved to file: {summary_file_path}")
    except Exception as e:
        print(f"Error saving summary to file: {e}")

    # Store the summary in ChromaDB
    add_chapter_version(chapters_collection, "chapter_1", chapter_summary, "summary")
    print("✅ Chapter summary stored in ChromaDB.")
    speak_text("Chapter summary stored in the database and saved to a text file.")
    
    # --- Step 6: (Optional) Calculate RL Reward based on human input ---
    print("\n--- Step 6: Calculating RL Reward ---")
    reward = calculate_reward(original_chapter_text, ai_rewrite, human_input)
    print(f"Calculated RL Reward for this iteration: {reward}")
    speak_text(f"Calculated a reward of {reward} for this iteration.")

    print("\n--- Workflow Complete ---")
    speak_text("Automated Book Publication Workflow complete. The final chapter version is ready for publication.")
    print("Final chapter version is ready for publication.")


if __name__ == "__main__":
    asyncio.run(automated_publication_workflow())

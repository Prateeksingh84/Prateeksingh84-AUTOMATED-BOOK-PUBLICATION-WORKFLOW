
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import os

from .scraping.scraper import scrape_chapter
from .llm_client import LLMService
from .agents.writer_agent import AIWriter
from .agents.reviewer_agent import AIReviewer
from .database.chromadb_manager import (
    initialize_chromadb,
    create_or_get_collection,
    add_chapter_version,
    get_chapter_versions,
    semantic_search_chapters
)

app = FastAPI(
    title="Automated Book Publication Workflow API",
    description="API for managing content scraping, AI rewriting, reviewing, and versioning.",
    version="0.1.0"
)

DATA_DIR = "data"
CHROMA_DB_PATH = "./chroma_db"
os.makedirs(DATA_DIR, exist_ok=True)


llm_service: LLMService | None = None
writer_agent: AIWriter | None = None
reviewer_agent: AIReviewer | None = None
chroma_client = None
chapters_collection = None


@app.on_event("startup")
async def startup_event():
    """
    Initializes clients when the FastAPI application starts.
    """
    global llm_service, writer_agent, reviewer_agent, chroma_client, chapters_collection
    print("API Startup: Initializing services...")
    
    try:
        llm_service = LLMService(model_name="gemini-1.5-pro")
        writer_agent = AIWriter(llm_service)
        reviewer_agent = AIReviewer(llm_service)

        chroma_client = initialize_chromadb(path=CHROMA_DB_PATH)
        chapters_collection = create_or_get_collection(chroma_client, "book_chapters")
        print("API Startup: All services initialized successfully.")
    except Exception as e:
        print(f"API Startup Error: Failed to initialize services: {e}")
        


# --- Request Models ---
class ScrapeRequest(BaseModel):
    url: str

class ReviewRequest(BaseModel):
    chapter_id: str
    human_input: str 

class SearchRequest(BaseModel):
    query: str
    n_results: int = 5


# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Automated Book Publication Workflow API. Visit /docs for API details."}

@app.post("/workflow/start")
async def start_workflow(request: ScrapeRequest):
    """
    Starts the automated publication workflow for a given URL.
    This initiates scraping, AI rewriting, and AI review.
    """
    if not writer_agent or not reviewer_agent or not chapters_collection:
        raise HTTPException(status_code=503, detail="AI services not initialized.")

    print(f"API: Starting workflow for URL: {request.url}")
    
    # 1. Scrape the URL
    scraped_file_path = await scrape_chapter(request.url, output_dir=DATA_DIR)
    if not scraped_file_path:
        raise HTTPException(status_code=500, detail="Failed to scrape content.")

    try:
        with open(scraped_file_path, "r", encoding="utf-8") as f:
            original_chapter_text = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Scraped content file not found on disk.")
    
    # Assuming chapter_id is derived from URL or title for simplicity
    chapter_id = os.path.basename(scraped_file_path).replace(".txt", "").replace("_screenshot", "")
    add_chapter_version(chapters_collection, chapter_id, original_chapter_text, "original")

    # 2. AI Writing
    ai_rewrite = writer_agent.rewrite_chapter(original_chapter_text)
    add_chapter_version(chapters_collection, chapter_id, ai_rewrite, "ai_draft_1")

    # 3. AI Review
    ai_review_feedback = reviewer_agent.review_rewrite(original_chapter_text, ai_rewrite)
    
    return {
        "status": "workflow_initiated",
        "chapter_id": chapter_id,
        "original_content_snippet": original_chapter_text[:200] + "...",
        "ai_draft_snippet": ai_rewrite[:200] + "...",
        "ai_review_feedback": ai_review_feedback
    }

@app.post("/workflow/human_review")
async def human_review(request: ReviewRequest):
    """
    Processes human input for a chapter, either approving the AI draft
    or incorporating human edits as the final version.
    """
    if not chapters_collection:
        raise HTTPException(status_code=503, detail="Database service not initialized.")

    
    chapter_versions = get_chapter_versions(chapters_collection, request.chapter_id)
    latest_ai_draft = None
    original_text = None

    for doc, meta in zip(chapter_versions['documents'], chapter_versions['metadatas']):
        if meta.get('version_type') == 'ai_draft_1':
            latest_ai_draft = doc
        if meta.get('version_type') == 'original':
            original_text = doc

    if not latest_ai_draft or not original_text:
        raise HTTPException(status_code=404, detail=f"AI draft or original for chapter {request.chapter_id} not found.")

    final_text = ""
    status_message = ""

    if request.human_input.lower() == "approve":
        final_text = latest_ai_draft
        status_message = "Human approved the AI draft. Stored as final."
    else:
        final_text = request.human_input 
        status_message = "Human provided new edits. Stored as final."
    
    add_chapter_version(chapters_collection, request.chapter_id, final_text, "final_draft")
    
    

    return {
        "status": status_message,
        "chapter_id": request.chapter_id,
        "final_content_snippet": final_text[:200] + "..."
    }

@app.get("/workflow/chapter_versions/{chapter_id}")
async def get_chapter_all_versions(chapter_id: str):
    """
    Retrieves all stored versions for a specific chapter ID.
    """
    if not chapters_collection:
        raise HTTPException(status_code=503, detail="Database service not initialized.")

    versions = get_chapter_versions(chapters_collection, chapter_id)
    
    formatted_versions = []
    for doc, meta, id_val in zip(versions['documents'], versions['metadatas'], versions['ids']):
        formatted_versions.append({
            "id": id_val,
            "version_type": meta.get('version_type'),
            "chapter_id": meta.get('chapter_id'),
            "content_snippet": doc[:200] + "..." 
        })
    
    return {"chapter_id": chapter_id, "versions": formatted_versions}

@app.post("/workflow/search_chapters")
async def search_chapters_api(request: SearchRequest):
    """
    Performs a semantic search across all stored chapter versions.
    """
    if not chapters_collection:
        raise HTTPException(status_code=503, detail="Database service not initialized.")
    
    results = semantic_search_chapters(chapters_collection, request.query, request.n_results)
    
    formatted_results = []
    for i in range(len(results['ids'])):
        formatted_results.append({
            "id": results['ids'][i],
            "distance": results['distances'][i],
            "version_type": results['metadatas'][i].get('version_type'),
            "chapter_id": results['metadatas'][i].get('chapter_id'),
            "content_snippet": results['documents'][i][:200] + "..."
        })
    return {"query": request.query, "results": formatted_results}



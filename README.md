📚 Automated Book Publication Workflow

LLM-powered pipeline that simulates a modern book-publishing flow—from web scraping chapters to AI rewriting, AI review, human approval, and versioned storage for publication.

Stack: Python 3.10+, Google Gemini (Generative AI), ChromaDB, SentenceTransformer, AsyncIO

🚀 Features

Web Scraping: Fetch chapter content from a URL (e.g., Wikisource) or use local files

AI Writing Agent: Creative rewrites via Gemini with configurable prompts

AI Reviewing Agent: Compares original vs. AI rewrite and gives structured feedback

Human-in-the-Loop: Approve or edit drafts before finalization

Version Control: Store original, AI drafts, human edits in ChromaDB with metadata + semantic search

Reproducibility: Saves prompt history, run logs, and outputs

🗂️ Project Structure

project/
├─ main.py                     # Orchestrates the full workflow
├─ prompts/
│  ├─ extraction_prompt.txt    # Content extraction / structuring
│  └─ review_prompt.txt        # Editorial review prompt
├─ utils/
│  ├─ pdf_parser.py
│  ├─ web_scraper.py
│  ├─ ai_writer.py             # Gemini interface (writer)
│  ├─ ai_reviewer.py           # Gemini interface (reviewer)
│  ├─ store.py                 # ChromaDB + embeddings
│  └─ io_helpers.py
├─ data/
│  ├─ downloaded/              # Raw scraped files
│  ├─ outputs/
│  │  ├─ drafts/               # AI + human drafts
│  │  ├─ final/                # Final approved drafts
│  │  └─ docs/                 # Prompt history, summaries
│  └─ chroma/                  # Persistent vector store
└─ README.md

⚙️ Setup
1) Install requirements
pip install google-generativeai chromadb sentence-transformers requests beautifulsoup4 python-dotenv

2) Configure environment
3) 
Create .env in project root:
GEMINI_API_KEY=your_google_generative_ai_key
MODEL_NAME=gemini-1.5-pro
EMBED_MODEL=all-MiniLM-L6-v2
CHROMA_DIR=./data/chroma

▶️ Usage
A) Scrape + Process a chapter from the web
python main.py \
  --source web \
  --url "https://wikisource.org/your-chapter-url" \
  --title "Chapter 01 - Beginnings"

B) Use a local text/PDF file
python main.py \
  --source file \
  --path "./data/downloaded/chapter01.txt" \
  --title "Chapter 01 - Beginnings"

C) Workflow steps (automated):

Scrape/Load original text → save to data/downloaded/

Initialize ChromaDB (persistent vector store)

AI Writer generates Draft v1

AI Reviewer produces editorial feedback

Human Review: approve or provide edits (CLI prompt)

Final Storage: store final_draft + metadata in ChromaDB and data/outputs/final/

🧠 Prompts

prompts/extraction_prompt.txt – guides structure (headings, summaries, key terms)

prompts/review_prompt.txt – instructs reviewer to compare fidelity, tone, clarity, and suggest edits

🧾 Example Console Output
--- Step 1: Scraping content from the web ---
Successfully scraped and read the original chapter text.

--- Step 2: Initializing ChromaDB for versioning ---
Original chapter version stored in ChromaDB.

--- Step 3: AI writing and review cycle ---
AI draft 1 created and stored.

AI Reviewer Feedback:
"The rewritten text flows better but loses some original context in paragraph 2.
Consider restoring the metaphors."

--- Step 4: Human-in-the-Loop review ---
Please provide your edits or 'approve':

🛠️ Troubleshooting

Auth errors: verify GEMINI_API_KEY and network access

Empty scrape: check the URL and update selectors in web_scraper.py

Model errors: switch MODEL_NAME or reduce context length

Chroma issues: delete data/chroma/ to rebuild the store

🗺️ Roadmap

Multi-draft iteration with scoring

YAML run manifests for full reproducibility

Optional OCR (for scanned PDFs)

Web UI (FastAPI + simple dashboard)

🙏 Acknowledgments

Google Gemini for generative capabilities

ChromaDB for local vector storage

SentenceTransformer for embeddings

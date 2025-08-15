# 📚 Automated Book Publication Workflow

## 🚀 Project Overview
This project is an **LLM-powered automated workflow** that simulates the book publishing pipeline — from web scraping chapters to AI-assisted rewriting, reviewing, versioning, and storing final drafts for publication.

The system orchestrates a pipeline where:
1. A chapter is scraped from an online source.
2. An AI writer rewrites the chapter creatively.
3. An AI reviewer critiques the AI-generated draft.
4. A human (optionally) edits or approves the AI version.
5. All versions are stored with metadata in **ChromaDB** for future access and tracking.

The project leverages:
- **Google's Gemini API** for content generation and review.
- **ChromaDB** for persistent versioning and semantic search.

---

## 🧠 Key Features
- ✅ **Web Scraping** – Automatically scrapes chapter content from a given URL.
- ✍️ **AI Writing Agent** – Rewrites the scraped content using LLMs (e.g., Gemini).
- 🧐 **AI Reviewing Agent** – Provides editorial feedback comparing the original and AI-rewritten version.
- 🧑‍💻 **Human-in-the-Loop** – Allows manual approval or editing of AI-generated drafts.
- 📦 **Version Control** – All versions (original, AI drafts, human edits) are stored in ChromaDB with semantic search support.

---

## 🔧 Technologies Used
- **Python 3.10+**
- **Google Generative AI (Gemini)**
- **ChromaDB** for local semantic versioning
- **SentenceTransformer** embeddings
- **AsyncIO** for orchestration

---

## 🛠️ How It Works

### 1. Scrape Chapter
- A chapter is downloaded from **Wikisource**.
- Stored in a local text file inside the `data/` folder.

### 2. Initialize ChromaDB
- Local persistent vector store setup using **SentenceTransformer** embeddings.

### 3. AI Writing
- The **writer agent** (`AIWriter`) rewrites the original text using a creative prompt.

### 4. AI Review
- The **reviewer agent** (`AIReviewer`) evaluates the AI rewrite and provides structured feedback.

### 5. Human Review
- A human can either approve the AI-generated draft or provide their own edited version.

### 6. Final Storage
- The final approved or edited version is stored as `final_draft` in ChromaDB.

---

## 🧪 Running the Project

### 1️⃣ Install Requirements
```bash
pip install google-generativeai chromadb sentence-transformers

### 2️⃣ Set Your Gemini API Key
```bash
export GEMINI_API_KEY=your_google_generative_ai_key

🧾 Example Output
--- Step 1: Scraping content from the web ---
Successfully scraped and read the original chapter text.

--- Step 2: Initializing ChromaDB for versioning ---
Original chapter version stored in ChromaDB.

--- Step 3: AI writing and review cycle ---
AI draft 1 created and stored.
AI Reviewer Feedback:
--- The rewritten text flows better but loses some original context in paragraph 2. Consider restoring the metaphors. ---

--- Step 4: Human-in-the-Loop review ---
Please provide your edits or 'approve':


📌 Notes

Make sure you have a valid Google Gemini API Key.

Internet connection is required for web scraping and API calls.

ChromaDB stores all versions locally for quick retrieval.


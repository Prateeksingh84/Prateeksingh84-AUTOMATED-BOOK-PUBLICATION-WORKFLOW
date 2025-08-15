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

### 📋 Prerequisites

Before you begin, ensure you have the following:

* **Python 3.x** installed.
* **Internet Connection:** Required for web scraping and making API calls to the AI model.
* **Google Gemini API Key:** You'll need a valid API key to interact with the Google Gemini model.
    * `let apiKey = "" // If you want to use models other than gemini-2.5-flash-preview-05-20 or imagen-3.0-generate-002, provide an API key here. Otherwise, leave this as-is.` - Ensure this line in your code uses your actual API key or the mechanism provided by Canvas for runtime injection.

### ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [your_repository_url_here]
    cd [your_repository_name]
    ```
2.  **Install dependencies:**
    This project will likely require libraries for web scraping (e.g., `BeautifulSoup4`, `requests`), AI interaction (e.g., `google-generativeai` or `requests` for direct API calls), and ChromaDB.
    ```bash
    pip install beautifulsoup4 requests chromadb python-dotenv  # Add other necessary libraries here
    ```
3.  **Set up your API Key:**
    It's recommended to use environment variables for your API key. Create a `.env` file in the root of your project:
    ```
    GOOGLE_GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
    ```
    Then, load it in your Python code using `os.getenv('GOOGLE_GEMINI_API_KEY')`.

---

## 💡 Usage

The system operates through a sequential workflow:

1.  **Scraping Content:** The process begins by scraping content from a specified web source.
2.  **Versioning Original:** The scraped original content is immediately stored as the first version in ChromaDB.
3.  **AI Drafting:** The AI generates an initial draft based on the original content. This draft is also stored in ChromaDB.
4.  **AI Review Cycle:** An AI reviewer provides feedback on the draft, aiming to refine the content. Subsequent drafts and their feedback are versioned.
5.  **Human-in-the-Loop Review:** A prompt for human intervention allows a user to review the AI-generated content and AI feedback.
6.  **Edits and Approval:** The human can then make necessary edits to restore context, improve flow, or apply specific nuances, finally approving the content.

The system ensures that every iteration and change is logged and retrievable, providing a complete history of content evolution.

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

---




# src/database/chromadb_manager.py

import chromadb
from chromadb.utils import embedding_functions
import os

def initialize_chromadb(path: str = "./chroma_db"):
    """
    Initializes a persistent ChromaDB client.
    Creates the directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)
    print(f"Initializing ChromaDB client at: {path}")
    return chromadb.PersistentClient(path=path)

def create_or_get_collection(client: chromadb.PersistentClient, collection_name: str):
    """
    Creates a new ChromaDB collection or gets an existing one.
    Uses a Sentence Transformer for embedding.
    """
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    print(f"Creating or getting ChromaDB collection: {collection_name}")
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=sentence_transformer_ef # type: ignore
    )

def add_chapter_version(
    collection: chromadb.api.models.Collection.Collection, 
    chapter_id: str, 
    chapter_text: str, 
    version_type: str,
    screenshot_path: str | None = None # New optional parameter for screenshot path
):
    """
    Adds a new version of a chapter to the ChromaDB collection,
    optionally including the path to its associated screenshot.

    Args:
        collection (chromadb.api.models.Collection.Collection): The ChromaDB collection object.
        chapter_id (str): A unique identifier for the chapter (e.g., "chapter_1").
        chapter_text (str): The content of the chapter version.
        version_type (str): The type of this version (e.g., "original", "ai_draft", "human_edited", "final_draft", "summary").
        screenshot_path (str | None): Optional path to the screenshot file on disk.
    """
    # Generate a unique ID for this specific version entry
    current_count = len(collection.get()['ids'])
    version_entry_id = f"{chapter_id}-{version_type}-{current_count + 1}"

    metadata = {"chapter_id": chapter_id, "version_type": version_type}
    if screenshot_path:
        metadata["screenshot_path"] = screenshot_path # Add screenshot path to metadata

    print(f"Adding version '{version_type}' for chapter '{chapter_id}' with ID '{version_entry_id}' to ChromaDB.")
    if screenshot_path:
        print(f"Associated screenshot path: {screenshot_path}")
        
    try:
        collection.add(
            documents=[chapter_text],
            metadatas=[metadata],
            ids=[version_entry_id]
        )
    except Exception as e:
        print(f"Error adding chapter version to ChromaDB: {e}")

def get_chapter_versions(collection: chromadb.api.models.Collection.Collection, chapter_id: str):
    """
    Retrieves all versions of a specific chapter from the database.
    """
    print(f"Retrieving all versions for chapter: {chapter_id}")
    results = collection.get(
        where={"chapter_id": chapter_id},
        include=['metadatas', 'documents']
    )
    return results

def semantic_search_chapters(collection: chromadb.api.models.Collection.Collection, query_text: str, n_results: int = 5):
    """
    Performs a semantic search on the chapter versions stored in the collection.
    """
    print(f"Performing semantic search for query: '{query_text}'")
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=['distances', 'metadatas', 'documents']
    )
    return results


# src/scraping/rl_reward.py

# This is a high-level, conceptual example of a reward function.
# A real implementation would involve a trained model or a more complex logic.
# It might also use more advanced NLP libraries for deeper analysis.

def calculate_reward(original_text: str, rewritten_text: str, human_feedback: str) -> float:
    """
    Calculates a reward based on the quality of a rewritten chapter.
    This function could be the core of an RL agent's learning process.
    - Positive reward for human approval or positive feedback.
    - Negative reward for rejection or negative feedback.
    - Reward based on the semantic similarity to the original text.

    Args:
        original_text (str): The original chapter text.
        rewritten_text (str): The AI-generated rewritten chapter text.
        human_feedback (str): Feedback provided by the human reviewer.

    Returns:
        float: A numerical reward value.
    """
    reward = 0.0
    
    # 1. Human Feedback Reward: Direct signal from the user
    # This is the most important signal in a human-in-the-loop system.
    if "approve" in human_feedback.lower():
        reward += 1.0  # High reward for approval
    elif "reject" in human_feedback.lower() or "poor" in human_feedback.lower():
        reward -= 1.0  # High penalty for rejection or strong negative feedback
    elif "good" in human_feedback.lower() or "minor" in human_feedback.lower():
        reward += 0.5 # Moderate reward for good or minor edits
    elif "needs work" in human_feedback.lower() or "major" in human_feedback.lower():
        reward -= 0.5 # Moderate penalty for needing significant work

    # 2. Semantic Similarity Reward: using embeddings to compare texts
    # This helps ensure the rewritten text remains true to the original meaning.
    try:
        from sentence_transformers import SentenceTransformer, util
        # Load a pre-trained sentence embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Encode texts into embeddings
        original_emb = model.encode(original_text, convert_to_tensor=True)
        rewrite_emb = model.encode(rewritten_text, convert_to_tensor=True)
        
        # Calculate cosine similarity
        cosine_score = util.pytorch_cos_sim(original_emb, rewrite_emb).item()
        
        # Add a scaled score for similarity (e.g., higher similarity = higher reward)
        # We can weigh this less than direct human feedback if desired.
        reward += cosine_score * 0.2  # Scaled by 0.2
    except ImportError:
        print("Warning: 'sentence-transformers' not installed. Skipping semantic similarity reward.")
    except Exception as e:
        print(f"Error calculating semantic similarity: {e}. Skipping this reward component.")

    # 3. Readability/Quality Heuristic (conceptual placeholder)
    # In a more advanced system, you might use text analysis libraries (e.g., textstat)
    # or another LLM call to score readability, grammar, or style.
    # For now, this is just a conceptual slot.
    # If the rewritten text is significantly shorter than original (and not approved), penalize.
    if len(rewritten_text) < len(original_text) * 0.7 and "approve" not in human_feedback.lower():
        reward -= 0.1 # Small penalty for significant text reduction without approval

    return reward


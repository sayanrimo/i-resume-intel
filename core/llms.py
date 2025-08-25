# core/llms.py

import os
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

def get_llm():
    """Initializes and returns the HuggingFaceEndpoint LLM."""
    
    api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # --- DEBUGGING STEP ---
    print("---" * 10)
    print("DEBUG: Attempting to load Hugging Face model.")
    if api_token:
        print(f"DEBUG: Found API Token starting with: {api_token[:5]}...")
    else:
        print("DEBUG: API Token NOT FOUND in environment!")
    print("---" * 10)
    # --- END DEBUGGING ---

    if not api_token:
        raise ValueError("Hugging Face API token not found. Please set the HUGGINGFACEHUB_API_TOKEN environment variable.")

    # We will use a highly reliable, smaller model for this final test
    repo_id = "google/flan-t5-base"
    
    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        temperature=0.5,
        max_new_tokens=1024,
        huggingfacehub_api_token=api_token
    )
    return llm
# app/views/upload.py
import streamlit as st
from pathlib import Path
import time

from core.ingestion import load_resume
from core.splitters import split_recursively
from core.embeddings import default_embedding_model
from core.vectordb import VectorDB
from core.nlp_extract import extract_entities
from core.summarizer import generate_summary
from core.rag import RAG_Pipeline
from core.models import Candidate

def process_resume(uploaded_file, uploads_dir: Path, indexes_dir: Path):
    """Saves, processes, and indexes a resume file."""
    # 1. Save the file
    file_path = uploads_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File '{uploaded_file.name}' uploaded successfully.")
    
    with st.spinner("Parsing resume..."):
        resume_data = load_resume(file_path)
        if not resume_data or not resume_data.get("text"):
            st.error("Could not parse text from the resume.")
            return

    raw_text = resume_data["text"]

    with st.spinner("Extracting key information using NLP..."):
        entities = extract_entities(raw_text)

    with st.spinner("Generating candidate summary with AI..."):
        summary = generate_summary(raw_text)
    
    # Store candidate info in session state
    st.session_state.candidate = Candidate(
        name=entities.get("name", "N/A"),
        email=entities.get("email", "N/A"),
        summary=summary,
        skills=entities.get("skills", []),
        raw_text=raw_text
    )

    with st.spinner("Chunking text and creating vector index..."):
        chunks = split_recursively(raw_text)
        index_name = file_path.stem
        index_path = str(indexes_dir / f"{index_name}.faiss")
        metadata_path = str(indexes_dir / f"{index_name}.pkl")
        
        vector_db = VectorDB(index_path, metadata_path, default_embedding_model)
        vector_db.build(chunks)
    
    st.session_state.rag_pipeline = RAG_Pipeline(vector_db)
    st.success("Resume processed and indexed! You can now view insights or ask questions.")

def render_upload_page(uploads_dir: Path, indexes_dir: Path):
    st.header("📄 Upload a New Resume")
    st.write("Upload a candidate's resume in PDF or DOCX format to begin analysis.")
    
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        if st.button("Analyze Resume"):
            process_resume(uploaded_file, uploads_dir, indexes_dir)
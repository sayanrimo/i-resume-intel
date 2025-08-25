import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path
from dotenv import load_dotenv  # <-- IMPORT THIS

# Load environment variables from .env file
load_dotenv()  # <-- ADD THIS LINE

# Import your core logic
from core.ingestion import parse_pdf, parse_docx
import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path

# Import your core logic
from core.ingestion import parse_pdf, parse_docx
from core.splitters import split_recursively
from core.embeddings import default_embedding_model
from core.vectordb import VectorDB
from core.nlp_extract import extract_entities
from core.summarizer import generate_summary
from core.qgen import generate_interview_questions
from core.rag import RAG_Pipeline
from core.models import Candidate, Skill

# --- PAGE CONFIG ---
st.set_page_config(page_title="i-Resume-Intel", layout="wide")

# --- PATHS ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
INDEXES_DIR = DATA_DIR / "indexes"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
INDEXES_DIR.mkdir(parents=True, exist_ok=True)

# --- SESSION STATE ---
if 'candidate' not in st.session_state:
    st.session_state.candidate = None
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- UI HELPER FUNCTIONS ---
def render_info_card(title: str, value: str):
    st.markdown(f"""
    <div style="border: 1px solid #4f515e; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
        <h5 style="margin: 0; color: #a1a3ab;">{title}</h5>
        <p style="margin: 5px 0 0 0; font-size: 1.1em;">{value if value else 'Not Found'}</p>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE RENDERING FUNCTIONS ---
def render_upload_page():
    st.header("📄 Upload a New Resume")
    uploaded_file = st.file_uploader("Upload a resume (PDF or DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

    if uploaded_file:
        if st.button("Analyze Resume"):
            file_path = UPLOADS_DIR / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Parsing and extracting text..."):
                raw_text = parse_pdf(file_path) if file_path.suffix == '.pdf' else parse_docx(file_path)
            
            if not raw_text:
                st.error("Could not extract text from the document.")
                return

            with st.spinner("Extracting entities..."):
                entities = extract_entities(raw_text)

            with st.spinner("Generating summary..."):
                summary = generate_summary(raw_text)

            st.session_state.candidate = Candidate(
                name=entities.get("name"),
                email=entities.get("email"),
                summary=summary,
                skills=[Skill(**s) for s in entities.get("skills", [])],
                raw_text=raw_text
            )

            with st.spinner("Creating vector index for Q&A..."):
                chunks = split_recursively(raw_text)
                index_name = file_path.stem
                vector_db = VectorDB(
                    str(INDEXES_DIR / f"{index_name}.faiss"),
                    str(INDEXES_DIR / f"{index_name}.pkl"),
                    default_embedding_model
                )
                vector_db.build(chunks)
                st.session_state.rag_pipeline = RAG_Pipeline(vector_db)
            
            st.success("Resume processed! Navigate to 'Candidate Insights' or 'Resume Q&A'.")

def render_insights_page():
    st.header("📊 Candidate Insights")
    if not st.session_state.candidate:
        st.warning("Please upload a resume first.")
        return

    candidate = st.session_state.candidate
    col1, col2 = st.columns(2)
    with col1: render_info_card("Candidate Name", candidate.name)
    with col2: render_info_card("Email Address", candidate.email)
    
    st.subheader("🤖 AI-Generated Summary")
    st.info(candidate.summary)

    st.subheader("🛠️ Extracted Skills")
    if candidate.skills:
        skill_tags = "".join(f"<span style='background-color: #262730; border-radius: 15px; padding: 5px 10px; margin: 3px; display: inline-block;'>{skill.name}</span>" for skill in candidate.skills)
        st.markdown(skill_tags, unsafe_allow_html=True)
    else:
        st.write("No skills extracted.")

    st.subheader("💡 Generated Interview Questions")
    if st.button("Generate Questions"):
        with st.spinner("Generating..."):
            questions = generate_interview_questions(candidate.raw_text)
            st.markdown(questions)

def render_qa_page():
    st.header("❓ Resume Q&A")
    if not st.session_state.rag_pipeline:
        st.warning("Please upload and process a resume first.")
        return

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the resume..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            response = st.session_state.rag_pipeline.ask(prompt)
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- MAIN APP LAYOUT ---
st.title("🚀 i-Resume-Intel")

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Upload Resume", "Candidate Insights", "Resume Q&A"],
        icons=["cloud-upload", "bar-chart-line", "patch-question"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Upload Resume":
    render_upload_page()
elif selected == "Candidate Insights":
    render_insights_page()
elif selected == "Resume Q&A":
    render_qa_page()
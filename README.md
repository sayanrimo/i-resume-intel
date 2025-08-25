# i-Resume-Intel 🚀

An intelligent resume analysis and querying application powered by RAG (Retrieval-Augmented Generation). This tool helps recruiters and hiring managers quickly extract key information, gain insights, and generate interview questions from candidate resumes.

## ✨ Features

-   **Flexible LLM Support**: Easily switch between OpenAI's API and free, local models via Ollama.
-   **Automated Info Extraction**: Pulls contact info, skills, experience, and education using NLP.
-   **AI-Powered Insights**: Generates a concise summary of the candidate's profile.
-   **Semantic Q&A**: Ask questions about the resume in natural language (e.g., "What was their role at Google?").
-   **Interview Question Generation**: Automatically creates relevant technical and behavioral questions based on the resume content.

## 🛠️ Tech Stack

-   **Backend & ML**: Python, LangChain
-   **UI**: Streamlit
-   **NLP**: spaCy, Hugging Face (Sentence Transformers)
-   **Vector Store**: FAISS
-   **LLMs**: OpenAI / Ollama (e.g., Llama 3)
-   **Deployment**: Docker

## ⚙️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/i-resume-intel.git](https://github.com/your-username/i-resume-intel.git)
    cd i-resume-intel
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    -   Copy the `.env.example` to a new file named `.env`.
    -   Fill in the required variables. Choose your `LLM_PROVIDER` ("openai" or "ollama") and add your `OPENAI_API_KEY` if needed.

4.  **Download NLP models:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

5.  **(If using Ollama) Install Ollama and pull a model:**
    -   Download from [ollama.com](https://ollama.com/).
    -   Run `ollama pull llama3:8b` in your terminal.

6.  **Run the Streamlit application:**
    ```bash
    streamlit run app/main.py
    ```
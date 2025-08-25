# app/views/qa.py
import streamlit as st

def render_qa_page():
    st.header("❓ Resume Q&A")

    if not st.session_state.get('rag_pipeline'):
        st.warning("Please upload and process a resume first to enable the Q&A feature.")
        return

    rag_pipeline = st.session_state.rag_pipeline

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question about the resume..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            response = rag_pipeline.ask(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
# app/views/insights.py
import streamlit as st
import pandas as pd
import plotly.express as px

from app.components.cards import render_info_card
from core.qgen import generate_interview_questions

def render_insights_page():
    st.header("📊 Candidate Insights")

    if not st.session_state.get('candidate'):
        st.warning("Please upload a resume first to see insights.")
        return

    candidate = st.session_state.candidate

    # --- Display Candidate Info ---
    col1, col2 = st.columns(2)
    with col1:
        render_info_card("Candidate Name", candidate.name)
    with col2:
        render_info_card("Email Address", candidate.email)

    # --- Display AI Summary ---
    st.subheader("🤖 AI-Generated Summary")
    st.info(candidate.summary)

    # --- Display Skills ---
    st.subheader("🛠️ Extracted Skills")
    if candidate.skills:
        skill_names = [skill.get('name') for skill in candidate.skills]
        
        # Display as tags
        skill_tags_html = "".join(f"<span style='background-color: #262730; border: 1px solid #4f515e; border-radius: 15px; padding: 5px 10px; margin: 3px; display: inline-block;'>{skill}</span>" for skill in skill_names)
        st.markdown(skill_tags_html, unsafe_allow_html=True)
        
        # Skill frequency chart (optional)
        df_skills = pd.DataFrame(candidate.skills)
        if not df_skills.empty:
            skill_counts = df_skills['name'].value_counts().reset_index()
            skill_counts.columns = ['Skill', 'Count']
            fig = px.bar(skill_counts, x='Count', y='Skill', orientation='h', title='Skill Mentions')
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("No specific skills were extracted.")

    # --- Interview Question Generator ---
    st.subheader("💡 Generated Interview Questions")
    if st.button("Generate Interview Questions"):
        with st.spinner("Generating questions..."):
            questions = generate_interview_questions(candidate.raw_text, num_questions=5)
            st.markdown(questions)
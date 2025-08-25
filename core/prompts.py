from langchain.prompts import PromptTemplate

qa_template = "Context: {context}\n\nQuestion: {question}\n\nAnswer:"
QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context", "question"])

summary_template = "Create a 3-sentence professional summary of this resume:\n\n{context}\n\nSummary:"
SUMMARY_PROMPT = PromptTemplate(template=summary_template, input_variables=["context"])

interview_question_template = "Based on this resume context, generate {num_questions} interview questions:\n\n{context}"
INTERVIEW_QUESTION_PROMPT = PromptTemplate(template=interview_question_template, input_variables=["context", "num_questions"])
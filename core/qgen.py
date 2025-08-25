from langchain.chains.llm import LLMChain
from core.prompts import INTERVIEW_QUESTION_PROMPT
from core.llms import get_llm

def generate_interview_questions(resume_text: str, num_questions: int = 5) -> str:
    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=INTERVIEW_QUESTION_PROMPT)
    return chain.run(context=resume_text, num_questions=num_questions)
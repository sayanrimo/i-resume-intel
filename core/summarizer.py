from langchain.chains.llm import LLMChain
from core.prompts import SUMMARY_PROMPT
from core.llms import get_llm

def generate_summary(resume_text: str) -> str:
    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=SUMMARY_PROMPT)
    return chain.run(context=resume_text)
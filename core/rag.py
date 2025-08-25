from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from core.vectordb import VectorDB
from core.prompts import QA_PROMPT
from core.llms import get_llm

class RAG_Pipeline:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db
        self.llm = get_llm()
        self.retriever = self.vector_db.index.as_retriever() if self.vector_db.index else None
        self.rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | QA_PROMPT
            | self.llm
            | StrOutputParser()
        )
    def ask(self, question: str) -> str:
        if not self.retriever:
            return "Vector database not initialized."
        return self.rag_chain.invoke(question)
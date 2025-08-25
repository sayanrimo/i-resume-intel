from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def split_recursively(text: str, chunk_size: int = 1000, chunk_overlap: int = 150) -> List[str]:
    if not text:
        return []
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)
from pydantic import BaseModel, Field
from typing import List, Optional

class Skill(BaseModel):
    name: str = Field(description="The name of the skill")

class Candidate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    summary: Optional[str] = Field(description="A brief summary of the candidate's profile.")
    skills: List[Skill] = []
    raw_text: str = Field(description="The full, unprocessed text from the resume.")
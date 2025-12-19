from pydantic import BaseModel
from typing import List, Optional

class PaperSection(BaseModel):
    section_id: str
    title: str
    content: str
    order: int

class ResearchPaper(BaseModel):
    paper_id: str
    title: str
    authors: List[str]
    abstract: str
    full_text: str
    year: Optional[int]
    venue: Optional[str]
    keywords: List[str]
    sections: List[PaperSection]
    references: List[str] = []   # ✅ FIX


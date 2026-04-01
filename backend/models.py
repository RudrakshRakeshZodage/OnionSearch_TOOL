from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class SearchRequest(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str] = []
    amount: int = 20
    include_images: bool = False

class ScrapedResult(BaseModel):
    title: str
    url: str
    description: str
    snippet: Optional[str] = None
    score: float = 0.0
    matched_keywords: List[str] = []
    metadata: Dict[str, str] = {}
    emails: List[str] = []
    documents: List[str] = []
    images: List[str] = []

class SearchTask(BaseModel):
    id: str
    status: str # "pending", "running", "completed", "failed"
    results: List[ScrapedResult] = []
    error: Optional[str] = None

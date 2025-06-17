from pydantic import BaseModel

class QueryInput(BaseModel):
    query: str

class FeedbackInput(BaseModel):
    feedback: str
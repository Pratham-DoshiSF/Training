from pydantic import BaseModel , Field

class QueryRequest(BaseModel):
    user_id: str = Field(..., example="16461")
    query: str = Field(..., example="What's the weather today?")


class FeedbackRequest(BaseModel):
    user_id: str = Field(..., example="16461")
    feedback: str = Field(..., example="I meant New York, not London.")
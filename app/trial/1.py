from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from conversation_bot.workflow.workflow import workflow, WorkflowRunner
from conversation_bot.utils_function.logger_utility import get_logger
from langchain_core.messages import ToolMessage
from typing import Optional

app = FastAPI()
logger = get_logger("FastAPI")

# In-memory session management
session_state = {
    "runner": None,
    "awaiting_feedback": False,
    "tool_call_id": None,
    "last_query": ""
}

# Thread Configuration for Production (replace with dynamic ID in prod)


# Initialize once
wf = workflow()
session_state["runner"] = WorkflowRunner(wf, "12354566")

# Request Models
class QueryInput(BaseModel):
    query: str

class FeedbackInput(BaseModel):
    feedback: str


@app.post("/query")
def handle_query(input_data: QueryInput):
    try:
        result = session_state["runner"].handle_query(input_data.query)

        if "__interrupt__" in result:
            tool_call = result["messages"][-1].tool_calls[0]
            session_state["awaiting_feedback"] = True
            session_state["tool_call_id"] = tool_call["id"]
            session_state["last_query"] = input_data.query

            clarification = tool_call["args"]["state"].get("messages", ["Clarification required"])[0]
            return {
                "status": "awaiting_feedback",
                "clarification": clarification
            }

        return {
            "status": "completed",
            "response": result["messages"][-1].content
        }

    except Exception as e:
        logger.error("Error in /query endpoint", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
def provide_feedback(input_data: FeedbackInput):
    if not session_state["awaiting_feedback"]:
        raise HTTPException(status_code=400, detail="No feedback expected at the moment.")

    try:
        tool_msg = ToolMessage(
            tool_call_id=session_state["tool_call_id"],
            content=input_data.feedback
        )

        result = session_state["runner"].resume_with_feedback(tool_msg)

        # Reset state
        session_state["awaiting_feedback"] = False
        session_state["tool_call_id"] = None
        session_state["last_query"] = ""

        return {
            "status": "completed",
            "response": result["messages"][-1].content
        }

    except Exception as e:
        logger.error("Error in /feedback endpoint", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

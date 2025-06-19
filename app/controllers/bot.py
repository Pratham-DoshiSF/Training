from typing import Dict

from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse

from app.schemas.bot import QueryRequest, FeedbackRequest
from conversation_bot.workflow.workflow import workflow, WorkflowRunner
from conversation_bot.utils_function.logger_utility import get_logger

logger = get_logger("FastAPI")
bot_router = APIRouter()

wf = workflow()

runner_store: Dict[str, WorkflowRunner] = {}

@bot_router.post("/query")
def handle_query(req: QueryRequest):
    try:
        if req.user_id not in runner_store:
            runner = WorkflowRunner(wf, req.user_id, True)
            runner_store[req.user_id] = runner
        else:
            runner = runner_store[req.user_id]

        result = runner.handle_query(req.query)

        if runner.check_for_interrupt():
            return JSONResponse(
                status_code=206,
                content={"status": "interrupted", "message": "Human input required."}
            )

        return {"status": "complete", "result": result["messages"][-1].content}

    except Exception as e:
        logger.error("Error in /query", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@bot_router.post("/feedback")
def handle_feedback(req: FeedbackRequest):
    try:
        runner = runner_store.get(req.user_id)
        if not runner:
            raise HTTPException(status_code=404, detail="Session not found. Start with /query first.")

        result = runner.resume_with_feedback(req.feedback)

        if runner.check_for_interrupt():
            return JSONResponse(
                status_code=206,
                content={"status": "interrupted", "message": "Further clarification needed."}
            )

        return {"status": "complete", "result": result["messages"][-1].content}

    except Exception as e:
        logger.error("Error in /feedback", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

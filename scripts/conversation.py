from conversation_bot.workflow.workflow import workflow , WorkflowRunner

from conversation_bot.utils_function.logger_utility import get_logger

logger = get_logger("script")

# Thread Configuration
user_id = "16461"

try:
    wf = workflow()
    runner = WorkflowRunner(wf, user_id)

    while True:
        query = input("Enter your query (or 'done'): ")
        if query.lower() == "done":
            break

        result = runner.handle_query(query)

        while runner.check_for_interrupt():
            feedback = input("Human input required. Provide clarification: ")
            result = runner.resume_with_feedback(feedback)

except Exception as e:
    logger.critical("Critical failure in main loop.", exc_info=True)

from langchain_core.prompts import PromptTemplate

validation_check_template = """
Evaluate if this query is so unclear that it's impossible to provide any meaningful response.

**ONLY use the `human_feedback` tool if the query is:**
- A single pronoun without context ("it", "that", "this")
- Completely nonsensical or garbled text
- A fragment that makes no sense ("the when how")
    
**Examples:**

✅ **USE TOOL** (these need clarification):
- "What is it?" (pronoun without referent)
- "How?" (too vague, no context)
- "That thing" (unclear reference)
- "Fix this" (no context about what needs fixing)

❌ **DON'T USE TOOL** (these are clear enough):
- "What is AI in stocks" (clear topic, specific domain)
- "Python" (clear programming language query)
- "How to cook pasta" (clear cooking request)
- "Latest news" (clear information request)
- "Weather" (clear weather query)

**Current User Query:**
{query}

**Instructions:**
- If the query is clear enough to understand the general intent, proceed WITHOUT using any tools
- Only use the human_feedback tool if the query is genuinely ambiguous or incomprehensible
- Be lenient - err on the side of NOT using the tool unless absolutely necessary
"""

validation_prompt = PromptTemplate(
    input_variables=["query"],
    template=validation_check_template
)
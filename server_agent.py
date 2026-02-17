from pydantic import BaseModel, Field
from uagents import Agent, Context, Protocol, Model
from langchain_groq import ChatGroq
 
CHAT_MODEL = "openai/gpt-oss-120b"
GROQ_API_KEY = ""
 
agent = Agent(name="groq_agent",
              seed="<moltbook_style",
              port=8000,
              network="testnet",
              endpoint=["http://127.0.0.1:8000/submit"]
              )
 
 
class AIRequest(BaseModel):
    question: str = Field(
        description="The question that the user wants to have an answer for."
    )
 
 
class AIResponse(BaseModel):
    answer: str = Field(
        description="The answer from AI agent to the user agent"
    )
 
 
PROMPT_TEMPLATE = """
Answer the following question:
{question}
"""
 
@agent.on_event("startup")
async def print_address(ctx: Context):
    ctx.logger.info(agent.address)
 
 
def query_groq_chat(prompt: str):
    llm = ChatGroq(
        api_key = GROQ_API_KEY,
        model = CHAT_MODEL,
        temperature=0.3
    )

 
    chat_completion = llm.invoke(prompt)
    return (chat_completion.content)
 
 
@agent.on_message(model=AIRequest, replies=AIResponse)
async def answer_question(ctx: Context, sender: str, msg: AIRequest):
    ctx.logger.info(f"Received question from {sender}: {msg.question}")
    prompt = PROMPT_TEMPLATE.format(question=msg.question)
    response = query_groq_chat(prompt)
    ctx.logger.info(f"Response: {response}")
    await ctx.send(
        sender, AIResponse(answer=response)
    )
 
agent.run()
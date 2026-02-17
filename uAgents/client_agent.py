from uagents import Agent, Context, Field, Model, Protocol
from pydantic import BaseModel, Field
 
agent = Agent(name="receiver agent",
              seed="i_see_it_coming",
              port=8001,
              endpoint=["http://127.0.0.1:8001/submit"]
              )
 
QUESTION = "Write the Javascript code to give me the sum from 1 to 10"
 
 
class AIRequest(BaseModel):
    question: str = Field(
        description="The question that the user wants to have an answer for."
    )
 
 
class AIResponse(BaseModel):
    answer: str = Field(
        description="The answer from AI agent to the user agent"
    )
 
 
@agent.on_event("startup")
async def ask_question(ctx: Context):
    ctx.logger.info(
        f"Asking AI agent to answer {QUESTION}"
    )
    # Paste server agent address here
    await ctx.send(
        'agent1q28u27lnhau7rpu2ya9epycqfnqayy7pe9tmxq2jxvmpacermmlw66ydjhp', AIRequest(question=QUESTION)
    )
 
 
@agent.on_message(model=AIResponse)
async def handle_data(ctx: Context, sender: str, data: AIResponse):
    ctx.logger.info(f"Got response from AI agent: {data.answer}")
 
agent.run()
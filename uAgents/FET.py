from uagents import Agent, Context
import cosmpy
 
from cosmpy.aerial.client import LedgerClient, NetworkConfig
 
agent = Agent(name="wallet", seed="token_to_wallet", port=8000, test=False,  network="testnet", endpoint=["http://localhost:8000/submit"])
 
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"ASI network address:{agent.wallet.address()}")
    ledger_client = LedgerClient(NetworkConfig.fetch_mainnet())
    address: str = agent.wallet.address()
    balances = ledger_client.query_bank_all_balances(address)
    ctx.logger.info(f"Balance of addr: {balances}")
 
if __name__ == "__main__":
    agent.run()
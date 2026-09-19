from langchain_mcp_adapters.client import MultiServerMCPClient
from rich import print as rprint
import asyncio

client = MultiServerMCPClient({
    "demo": {
        "url": "http://localhost:8001/mcp",
        "transport": "streamable_http",
    }
})

async def main():
    tools = await client.get_tools()  # 自动获取 add、multiply 等工具
    return tools


tools = asyncio.run(main())
rprint(tools)
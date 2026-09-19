      
"""
    测试：使用Agents调用MCP工具
"""
import asyncio

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from rich import print as rprint

load_dotenv()

# 创建MCP客户端对象
client = MultiServerMCPClient(
    {
        "12306-mcp": {
            "transport": "streamable_http",
            "url": "https://mcp.api-inference.modelscope.net/c57d5552d15849/mcp"
        }
    }
)

# 创建大模型对象
llm = ChatOpenAI(model="qwen-flash")

async def main():
    # 获取工具
    tools = await client.get_tools()
    # 创建智能体agent
    agent = create_agent(
        model=llm,
        tools=tools,
    )
    # 异步调用智能体
    result = await agent.ainvoke(
        {
            "messages":[
                ("user", "查询今天从北京到武汉的火车票")
            ]
        }
    )
    # print(result["messages"][-1].content)
    rprint(result)

if __name__ == "__main__":
    asyncio.run(main())

    
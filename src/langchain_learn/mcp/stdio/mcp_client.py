"""
┌─────────────────────┐         stdio (stdin/stdout)        ┌─────────────────────┐
│   mcp_server.py     │ ◄─────────────────────────────────► │   文件2 (client)     │
│   FastMCP("Demo")   │                                     │   ClientSession      │
│                     │                                     │                      │
│  @mcp.tool()        │  ◄── list_tools / call_tool ──────  │  1. initialize       │
│  @mcp.resource()    │  ◄── list_resources / read_resource │  2. 探测能力          │
│  @mcp.prompt()      │  ◄── list_prompts / get_prompt ───  │  3. 逐个调用          │
└─────────────────────┘                                     └─────────────────────┘
"""

import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from rich import print as rprint

async def stdio_run():
    server_params = StdioServerParameters(
        command="uv", 
        args=["run", "python", "src/langchain_learn/mcp/stdio/mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            # 获取可用工具
            tools = await session.list_tools()
            rprint(tools)
            print()

            # 调用工具
            call_res = await session.call_tool("add", {"a": 1, "b": 2})
            rprint(call_res)
            print()

            # 获取可用资源
            resources = await session.list_resources()
            rprint(resources)
            print()

            # 调用资源
            read_res = await session.read_resource("greeting://default")
            rprint(read_res)
            print()

            # 获取可用提示
            prompts = await session.list_prompts()
            rprint(prompts)
            print()

            # 调用提示
            get_res = await session.get_prompt("greet_user", {"name": "Jack"})
            rprint(get_res)
            print()

asyncio.run(stdio_run())
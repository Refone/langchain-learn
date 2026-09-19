import asyncio
from mcp.client.streamable_http import streamable_http_client, streamablehttp_client
from mcp import ClientSession

SERVER_URL = "http://127.0.0.1:8001/mcp"

async def http_run():
    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            # 初始化连接（无状态模式下也必须调用，但不需要握手）
            await session.initialize()

            # 1. 获取工具列表
            tools = await session.list_tools()
            print("=== Tools ===")
            for t in tools.tools:   
                print(f"  {t.name}: {t.description}")
            print()

            # 2. 调用工具
            result = await session.call_tool("add", {"a": 3, "b": 4})
            print("=== call_tool('add', 3, 4) ===")
            print(f"  {result.content[0].text}")
            print()

            result2 = await session.call_tool("multiply", {"a": 5, "b": 6})
            print("=== call_tool('multiply', 5, 6) ===")
            print(f"  {result2.content[0].text}")
            print()

            # 3. 读取资源
            resource = await session.read_resource("greeting://default")
            print("=== read_resource ===")
            print(f"  {resource.contents[0].text}")
            print()

            # 4. 获取提示
            prompt = await session.get_prompt("greet_user", {"name": "Alice", "style": "formal"})
            print("=== get_prompt ===")
            print(f"  {prompt.messages[0].content.text}")

if __name__ == "__main__":
    asyncio.run(http_run())
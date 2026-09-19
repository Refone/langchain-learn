from mcp.server.fastmcp import FastMCP

"""
npx @modelcontextprotocol/inspector python path/to/mcp_server.py
npx @modelcontextprotocol/inspector python src/langchain_learn/mcp/stdio/mcp_server.py
"""
# 创建 MCP 实例
mcp = FastMCP("Demo")
    
# 为 MCP 实例添加工具
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

# 为 MCP 实例添加资源
@mcp.resource("greeting://default")
def get_greeting() -> str:
    return "Hello from static resource!"

# 为 MCP 实例添加提示词
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
        "casual": "写一句轻松的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
from mcp.server.fastmcp import FastMCP

# 创建 MCP 实例，指定监听地址和端口
mcp = FastMCP(
    "Demo-HTTP",
    host="0.0.0.0",       # 允许外部访问
    port=8001,             # 监听端口
    stateless_http=True,   # 无状态模式，每个请求独立处理，简化测试
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@mcp.resource("greeting://default")
def get_greeting() -> str:
    return "Hello from Streamable HTTP resource!"

@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"

if __name__ == "__main__":
    # 启动 Streamable HTTP 服务
    mcp.run(transport="streamable-http")
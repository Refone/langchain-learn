"""
    大模型工具调用最小流程:
    1. 注册工具
    2. 第一次请求模型, 模型如果想调用工具, respose.tool_call 会有东西
    3. 替大模型去调用工具,获得返回结果, 将 ToolMessage append 到历史消息中
    4. 模型根据带有 ToolMessage 的第二次请求, 再给到最终的输出结果
"""
from langchain.messages import HumanMessage, ToolMessage
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain.tools import tool
from rich import print as rprint
from common import deepseek as model

# 有这个 tool 修饰符, 才能传入 tool_call 结构体, 才能 调用 invoke()
# 默认会从文档注释中提取信息, (文档注释有杨哥格式要求), 
# 或者从 @tool(description='...') 提取信息
@tool(parse_docstring=True)
def get_weather(city: str):
    """
    获取天气的工具
    
    Args:
        city: 城市
    """
    return f"{city}天气晴朗~"

rprint(convert_to_openai_tool(get_weather))
print('='*50)

# 将模型和工具绑定
model_with_tools = model.bind_tools([get_weather])

# 声明一个消息列表
messages = [
    HumanMessage("今天北京天气如何")
]

# 模型生成调用工具请求
response = model_with_tools.invoke(messages)

# 添加AIMessage到消息列表中
messages.append(response)

rprint(response)
print('='*50)

tool_calls = response.tool_calls

for tool_call in tool_calls:
    if tool_call["name"] == "get_weather":
        # 大模型和Agent的主要区别在于：大模型不会主动的调用工具，所以这时候我们需要主动让工具调用。
        # 返回的是ToolMessage类型消息，添加到消息列表中
        tool_response = get_weather.invoke(tool_call)
        messages.append(tool_response)

rprint(messages)
print('='*50)

final_response = model_with_tools.invoke(messages)
rprint(f"final_response: \n{final_response}")
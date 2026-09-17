from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import SystemMessage, HumanMessage
from rich import print as rprint

# 示例 1: 使用 BaseMessage（已实例化的消息）
system_msg = SystemMessage(content="你是一个AI工程师。")
human_msg = HumanMessage(content="你好！")

# 示例 2: 使用 BaseMessagePromptTemplate
system_prompt = SystemMessagePromptTemplate.from_template("你是一个{role}.")
human_prompt = HumanMessagePromptTemplate.from_template("{user_input}")

# 示例 3: 使用 BaseChatPromptTemplate（嵌套的 ChatPromptTemplate）
nested_prompt = ChatPromptTemplate.from_messages([("system", "嵌套提示词")])

prompt = ChatPromptTemplate.from_messages([
    system_msg,     # MessageLike (BaseMessage)
    human_msg,      # MessageLike (BaseMessage)
    system_prompt,  # MessageLike (BaseMessagePromptTemplate)
    human_prompt,   # MessageLike (BaseMessagePromptTemplate)
    nested_prompt,  # MessageLike (BaseChatPromptTemplate)
])

res = prompt.invoke({"role":"人工智能专家","user_input":"介绍一下大模型的应用场景"})
rprint(res)
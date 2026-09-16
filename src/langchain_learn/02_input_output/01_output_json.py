"""
    测试:模型输出结果 -> json 格式
    json 有两种格式:
    1. json 对象, {key: value, key:value, ...}
    2. json 数组, [value1, value2, ...]
"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="deepseek-flash")

# 调用模型
result = llm.invoke(
    [
        ("system", "要求输出json格式的结果，其中包含prime信息，表示所有的素数，数组类型；包含count信息，表示素数的数量，数值类型"),
        ("user", "帮我查询1-500之间所有的素数以及素数的数量")
    ]
)

print(result.content)
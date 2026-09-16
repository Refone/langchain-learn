"""
    OpenAI原生API设置格式化输出
"""
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

# 创建模型对象
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# 创建模型类
class JieRi(BaseModel):
    jieri: list[str]
    descriptions: list[str]

# 调用模型
result = client.chat.completions.parse(
    model="qwen-flash",
    messages=[
        {"role":"user", "content":"查询一年中比较重要的节日，以及节日的描述"}
    ],
    response_format=JieRi
)

print(result.choices[0].message.content)
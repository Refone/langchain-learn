"""
    测试: 使用 StrOutputParser 格式化输出
"""

from typing import List

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()

# 创建模型对象
llm = ChatOpenAI(model='qwen-flash')

# 调用模型
result = llm.invoke('给我讲一个笑话')

# 创建格式化对象
parser = StrOutputParser()

# 对模型输出的结果进行格式化
str_result = parser.invoke(result)

print(str_result)
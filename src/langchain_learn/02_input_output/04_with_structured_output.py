"""
    测试：LangChain中使用with_structured_output()输出格式化
"""
from typing import List
from rich import print as rprint
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()

# 创建模型对象
llm = ChatOpenAI(model="qwen-flash")

# 创建模型类
class JieRi(BaseModel):
    jieri: List[str]
    date: List[str]

# 提供 with_structed_output() 指定格式化输出结构
llm = llm.with_structured_output(schema=JieRi)

# 调用大模型
result = llm.invoke(
    [
        {"role":"user", "content":"查询一年中会放假的节日, 以及放假时长"}
    ]
)

rprint(result)

"""
JieRi(
    jieri=['元旦', '春节', '清明节', '劳动节', '端午节', '中秋节', '国庆节'],
    date=[
        '2024-01-01',
        '2024-02-10',
        '2024-02-11',
        '2024-02-12',
        '2024-02-13',
        '2024-02-14',
        '2024-02-15',
        '2024-04-04',
        '2024-04-05',
        '2024-04-06',
        '2024-05-01',
        '2024-05-02',
        '2024-05-03',
        '2024-06-10',
        '2024-09-17',
        '2024-09-18',
        '2024-09-19',
        '2024-10-01',
        '2024-10-02',
        '2024-10-03',
        '2024-10-04',
        '2024-10-05',
        '2024-10-06',
        '2024-10-07'
    ]
)
"""
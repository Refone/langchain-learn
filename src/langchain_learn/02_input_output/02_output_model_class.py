"""
    测试：格式化模型输出的结果为json格式（优化提示词）
    json有两种格式：
    1、json对象,{key:value,key:value,...}
    2、json数组,[value1,value2,...]
"""
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

# 创建模型对象
llm = ChatOpenAI(model="deepseek-flash")

# 创建模型类
class Prime(BaseModel):
    prime: list[int] = Field(description="存储所有的素数")
    count: int = Field(description="素数的个数")

# 获取输出格式解析器
parser = JsonOutputParser(pydantic_object=Prime)

# 获取解析器的说明信息
print('解析器说明', parser.get_format_instructions())

# 调用模型
result = llm.invoke(
    [
        ("system", parser.get_format_instructions()),
        ("user", "帮我查询1-500之间所有的素数以及素数的数量")
    ]
)

print(result.content)
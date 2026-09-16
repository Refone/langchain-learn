"""
    测试: 使用 PromptTemplate 处理提示词模板,
    调用大模型对象处理提示词,使用 StrOutputParser 格式化输出
"""
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# 创建 PromptTemplate 对象
prompt_template = PromptTemplate.from_template("将{text}翻译为英文")

# 模板占位符赋值
prompt = prompt_template.invoke({
        "text": "就是现在"
        })

# 创建大模型对象
llm = ChatOpenAI(model="qwen-flash")

# 调用模型
result = llm.invoke(prompt)

# 创建格式化对象
parser = StrOutputParser()

# 格式化输出
final = parser.invoke(result)

print(final)
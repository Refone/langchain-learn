"""
    LCEL: LangChain Expression Language
    从 Runable 构建新的 Runable
"""

from langchain_openai import ChatOpenAI


import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

# 1、初始化模型
llm = ChatOpenAI(
    model="qwen-flash"
)

# 2、创建两个并行运行的chain：使用两个不同的模型回答同一个问题，用以对比结果
paragraph_1_chain = (
    PromptTemplate.from_template("对这首诗{poem}做一下赏析，分析它蕴含的含义") | llm | StrOutputParser()
)
paragraph_2_chain = (
    PromptTemplate.from_template("对这首诗{poem}做一下赏析，分析它蕴含的意境") | llm | StrOutputParser()
)

# 3、对前面的两个chain的结果进行分析总结
summary_chain = (
    PromptTemplate.from_template("这两种赏析，第一种：{paragraph_1}，第二种：{paragraph_2}，进行总结") | llm | StrOutputParser()
)

# 4、构造LCEL：将前面的两个chain并行运行，然后将结果传递给summary_chain
map_chain = {
    "paragraph_1": paragraph_1_chain,
    "paragraph_2": paragraph_2_chain,
} | summary_chain

poem= """
菩提本无树，
明镜亦非台，
本来无一物，
何处惹尘埃。
"""

# 5、运行LCEL
resp = map_chain.invoke({"poem": poem})
print(resp)
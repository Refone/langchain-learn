"""
    测试: 提示词模版
"""
from typing import List

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

# Method 1.
prompt_template = ChatPromptTemplate.from_template("请评价{product}的优缺点, 包括{aspect1}和{aspect2}.")

# Method 2.
prompt_template = ChatPromptTemplate.from_messages(
    [
        {"role":"system", "content":"你是一个专业的评论家"},
        {"role":"user", "content":"请评价{product}的优缺点,包括{aspect1}和{aspect2}."}
    ]
)

# Method 3.
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个专业的评论家"),
        ("user", "请评价{product}的优缺点,包括{aspect1}和{aspect2}.")
    ]
)

# 对提示词占位符进行赋值
prompt = prompt_template.invoke(
    {
        "product" : "Macbook Pro M1 2021",
        "aspect1": "性能",
        "aspect2": "性价比"
    }
)

model = ChatOpenAI(model="qwen-flash")

result = model.invoke(prompt)

print(result.text)
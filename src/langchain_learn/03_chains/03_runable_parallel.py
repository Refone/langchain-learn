from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

model = ChatDeepSeek(
    model='deepseek-flash',
    extra_body={
        "thinking": {
            "type": "disabled"
        }
    }
    )

# 创建两条翻译链
en_chain = PromptTemplate.from_template('将{text}翻译为英语') | model | StrOutputParser()
jp_chain = PromptTemplate.from_template('将{text}翻译为日语') | model | StrOutputParser()

# 将 en_chain 和 jp_chain 合并为一个 RunableParallel 对象
chain = RunnableParallel(en=en_chain, jp=jp_chain)

# 执行双链对象
result = chain.invoke(
    {
        'text': '原来如此'
    }
)

print(result)
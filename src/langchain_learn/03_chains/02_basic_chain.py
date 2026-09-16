from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek

load_dotenv()

prompt_template = PromptTemplate.from_template("将这句话翻译为英语:{text}")
model = ChatDeepSeek(model='deepseek-flash')
parser = StrOutputParser()

chain = prompt_template | model | parser

result = chain.invoke(
    {
        "text": "最近过的怎样?"
    }
)

print(result)
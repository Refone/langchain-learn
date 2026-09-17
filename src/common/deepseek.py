from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

load_dotenv()

deepseek = ChatDeepSeek(
    model='deepseek-flash'
)
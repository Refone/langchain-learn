from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from rich import print as rprint

# 从.env文件中加载环境变量
load_dotenv(override=True)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

# 1. 初始化模型
model = init_chat_model(
    model="deepseek-flash",
    model_provider="deepseek",
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    temperature=0.2,
    max_tokens=500,
    # 指定可调整参数
    configurable_fields=("model", "model_provider", "temperature", "max_tokens"),
)

# 2. 准备 config 字典
config = {
    "run_name": "joke_generation",  # 在LangSmith中这次运行会显示为 "joke_generation"
    "tags": ["my_tag1", "my_tag2"],  # 打上标签便于分类查找
    "metadata": {
        "user_id": "shkstart",     # 记录用户ID
        "session_id": "sess_123"   # 记录会话ID
    },
    "configurable": {
        "model": "deepseek-v4-pro",  # 配置模型参数
        "model_provider": "openai",  # 配置模型提供商参数
        "temperature": 0.7,  # 配置温度参数
        "max_tokens": 1000  # 配置最大令牌数
    }
}

# 3. 调用模型并传入config
response = model.invoke(
    "1 + 2 = ？",
    config=config
)

rprint(response)
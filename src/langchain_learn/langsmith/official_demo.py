from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model='deepseek-flash',
    model_provider='deepseek',
    extra_body={
        "thinking": {
            "type": "disabled"
        }
    }
)

answer = model.invoke('你是谁?')

print(answer)
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model="deepseek-flash",
    extra_body={"thinking": {"type": "disabled"}}
)

hello_text = model.invoke("一句话介绍一下你自己.").text

print('欢迎使用 Chatbot 机器人, 退出请输入 q, 马上连入机器人...')
print(hello_text)

messages = [
    ("system", "你是一个通用聊天机器人, 友好 AI 助手")
]

while True:
    user_input = input("\n- (输入问题, 输入'q'退出):\n")
    if user_input == 'q':
        print("欢迎下次使用")
        break

    messages.append(
        ("user", user_input)
    )

    print("\nChatbot:\n", end="", flush=True)

    reply_text = ''

    for chunk in model.stream(messages):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            reply_text += chunk.content

    messages.append(
        ("assistant", reply_text)
    )

    print()
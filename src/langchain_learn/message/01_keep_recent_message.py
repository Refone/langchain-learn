from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

def keep_recent_messages(messages,max_pairs = 3):
    """
    保留最近的N轮对话
    max_pairs : 保留对话的轮数 （每轮 = user + assistant）
    """

    # 分离system 消息和对话消息
    system_messages = [m for m in messages if m.get("role") == "system"]
    conversation_messages = [m for m in messages if m.get("role") != "system"]

    # 只保留最近的消息对
    recent_messages = conversation_messages[-(max_pairs * 2):]

    # 返回系统消息和最近的消息对
    return system_messages + recent_messages

def long_talk():
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

    # 初始化
    long_conversation = [
        {"role": "system", "content": "你是 Python 导师"}
    ]

    # 第 1 轮
    long_conversation.append({"role": "user", "content": "什么是列表？用一句解释"})
    r1 = model.invoke(long_conversation)
    long_conversation.append({"role": "assistant", "content": r1.content})

    # 第 2 轮
    long_conversation.append({"role": "user", "content": "列表和元组有什么区别？用一句解释"})
    r2 = model.invoke(long_conversation)
    long_conversation.append({"role": "assistant", "content": r2.content})

    # 第 3 轮
    long_conversation.append({"role": "user", "content": "什么是字典呢？用一句解释"})
    r3 = model.invoke(long_conversation)
    long_conversation.append({"role": "assistant", "content": r3.content})

    print(f"原始消息数: {len(long_conversation)}")  # 7

    # 优化：只保留最近 2 轮
    optimized = keep_recent_messages(long_conversation, max_pairs=2)

    print(f"优化后消息数: {len(optimized)}")  # 5
    print(f"保留的内容: system + 最近2轮对话")

    # 添加新的用户问题
    optimized.append({"role": "user", "content": "我第一个问题问的是什么？"})
    # 使用优化后的历史
    response = model.invoke(optimized)
    print(f"\nAI 回复: {response.content}")

if __name__ == "__main__":
    long_talk()
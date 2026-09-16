from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import asyncio
import time

# 从.env文件中加载环境变量
load_dotenv(override=True)

model = init_chat_model(
    model='deepseek-flash'
)


async def consume_stream(stream_resp, start_time):
    """任务1：消费流式输出，每收到一个 token 就打印"""
    print(">>> [流式任务] 开始读取流式结果...")
    print(">>> [流式输出] ", end="", flush=True)
    async for chunk in stream_resp:
        content = chunk.content if hasattr(chunk, 'content') else str(chunk)
        # 加上时间戳前缀，直观看到 token 到达的时刻
        print(f"[{time.perf_counter() - start_time:5.2f}s|token]{content}", end="", flush=True)
    print("\n>>> [流式任务] 流式输出结束")


async def do_other_work(start_time):
    """任务2：模拟其他并发任务（sleep 打印）"""
    for i in range(20):
        await asyncio.sleep(1)  # 挂起自己，把事件循环让给流式任务
        print(f"\n>>> [并发任务] 正在执行第{i + 1}个任务... (已耗时 {time.perf_counter() - start_time:.2f}s)")


async def demo_async_stream():
    """演示异步调用的非阻塞特性"""
    print("=== 演示：astream 的异步（非阻塞）效果 ===")
    start_time = time.perf_counter()
    print("程序开始...")

    # 1. 发起异步流式请求（返回异步生成器，此时还没真正消费）
    print(">>> 发起异步流式调用 (astream)...")
    stream_resp = model.astream("解释机器学习的基本概念。")

    # 2. 关键改动：用 gather 让两个任务并发执行
    #    事件循环会在 sleep 挂起时去接收网络数据（打印 token），
    #    在等待网络数据时去执行 sleep 任务 —— 输出自然交叉
    print(">>> 两个任务并发启动，输出将交叉出现...")
    await asyncio.gather(
        consume_stream(stream_resp, start_time),
        do_other_work(start_time),
    )

    print(f"\n=== 总运行耗时: {time.perf_counter() - start_time:.2f}s ===")


async def main():
    await demo_async_stream()


if __name__ == "__main__":
    asyncio.run(main())
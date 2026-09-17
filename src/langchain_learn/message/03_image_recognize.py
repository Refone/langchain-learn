import os
import base64
import httpx
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

# 2. 初始化模型，使用支持视觉的模型 ID
model = ChatDeepSeek(
    model="deepseek-flash",  # 原生视觉模型
    # 如果仍遇到 thinking 参数警告，可在此处传递 extra_body
    # extra_body={"thinking": {"type": "disabled"}}
)

# 3. 准备图片（这里以网络图片为例，下载并转为 base64）
# DeepSeek API 通常不支持直接传 URL，需要 base64 编码
image_url = "https://img1.baidu.com/it/u=1715540369,4012013286&fm=253&app=138&f=JPEG?w=500&h=666"
image_data = base64.b64encode(httpx.get(image_url).read()).decode("utf-8")

# 4. 构建多模态消息
message = HumanMessage(
    content=[
        {"type": "text", "text": "请详细描述这张图片的内容。"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
        },
    ]
)

# 5. 调用模型
response = model.invoke([message])
print(response.content)
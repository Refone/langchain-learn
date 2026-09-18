"""
    测试: 使用 HuggingFaceEmbeddings 将文本转换为稠密向量
"""

from langchain_community.embeddings import HuggingFaceEmbeddings

# 创建对象
model = HuggingFaceEmbeddings(
    model_name="/Users/refone/Coding/ai/bge-m3",
)

# 使用本地嵌入模型, 将数据转换为稠密向量
result = model.embed_query("你好, 世界")
print(len(result))
print(result)

results = model.embed_documents([
    "hello, LangChain",
    "hello, LangGraph"
    ])

for result in results:
    print(result)
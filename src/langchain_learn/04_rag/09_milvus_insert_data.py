"""
    测试: 向 Milvus 添加数据
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np
from pymilvus import DataType, MilvusClient
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from FlagEmbedding import BGEM3FlagModel

# 创建 Milvus 客户端对象
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")

# 向 Milvus 添加数据
def insert_data(milvus_client: MilvusClient, collection_name: str):
    # 加载文档
    documents = UnstructuredWordDocumentLoader(
        file_path='/Users/refone/Desktop/math.docx'
    ).load()

    # 进行文档的切分
    chunks = RecursiveCharacterTextSplitter(
        separators = ["\n\n", "\n", "！", "？", "。", ""],  # 分隔符列表
        chunk_size=400,         # 每个切片的最大长度
        chunk_overlap=50,       # 重叠长度
        length_function=len,    # 获取切片长度的函数
        add_start_index=True,   # 在元数据中添加 start_index 起始索引
    ).split_documents(documents)

    # 创建嵌入模型 bge-m3 对象
    model = BGEM3FlagModel(
        model_name_or_path='/Users/refone/Coding/ai/bge-m3'
    )

    # 将 chunks (List[Document]) 中每个切片的文本内容取出, 存储到一个列表中
    sentences = [ doc.page_content for doc in chunks ]

    # 对每个切片中的文本转换为向量
    result = model.encode(
        sentences=sentences,
        return_dense=True,
        return_sparse=True
    )

    # 分别获取转换之后的 稠密向量 和 稀疏向量
    dense_vectors = result["dense_vecs"]
    sparse_vectors = result["lexical_weights"]

    # 创建储存最终数据的列表
    data = []

    # Method 1. 直接遍历
    # for index, chunk in enumerate(chunks):
    #     t = chunk.page_content
    #     m = chunk.metadata
    #     dv = dense_vectors[index]
    #     sv = sparse_vectors[index]

    # Method 2. zip
    for c, dv, sv in zip(chunks, dense_vectors, sparse_vectors):
        data.append(
            {
                "text": c.page_content,
                "metadata": c.metadata,
                "dense_vector": np.array(dv, dtype=np.float32),
                "sparse_vector": sv,
            }
        )

    milvus_client.insert(
        collection_name=collection_name,
        data=data
    )

if __name__ == "__main__":
    milvus_client = get_milvus_client()
    insert_data(milvus_client, "demo")
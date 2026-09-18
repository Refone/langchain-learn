"""
    测试 Milvus 进行向量检索
"""
import numpy as np
from pymilvus import MilvusClient
from FlagEmbedding import BGEM3FlagModel
from rich import print as rprint

# 创建 Milvus 客户端对象
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")

# 将用户的问题转换为向量
def embed_query(query: str):
    model =BGEM3FlagModel(model_name_or_path="/Users/refone/Coding/ai/bge-m3")
    result = model.encode([query],
                          return_dense=True,
                          return_sparse=True,
                          )
    return np.array(result["dense_vecs"], np.float32), result["lexical_weights"]

# 稠密向量检索
def search_dense_vector(milvus_client: MilvusClient, collection_name: str, query: str):
    # 获取 query 所对应的稠密向量
    dense_vector, _ = embed_query(query)
    # 进行稠密向量检索
    result = milvus_client.search(
        collection_name=collection_name,
        data=dense_vector,
        anns_field="dense_vector",
        # metric_type="L2",
        search_params={"metric_type": "L2"},
        limit=3,
        output_fields=["id", "text", "metadata"],
    )
    return result
    """
    [
        {id:___, distance:___, entity:{id:___, text:___, metadata:___}},    # 一个 Hit 对象
        {id:___, distance:___, entity:{id:___, text:___, metadata:___}},
        ...
    ]
    """

# 稀疏向量检索
def search_sparse_vector(milvus_client: MilvusClient, collection_name: str, query: str):
    # 获取 query 所对应的稠密向量
    _, sparse_vector = embed_query(query)
    # 进行稠密向量检索
    result = milvus_client.search(
        collection_name=collection_name,    # 集合名称
        data=sparse_vector,                 # 要检索的向量
        anns_field="sparse_vector",         # 要进行相似度比较的字段
        # metric_type="L2",
        search_params={"metric_type": "IP"},    # 比较相似度的方式
        limit=3,                                # 设置检索结果的最大条数
        output_fields=["id", "text", "metadata"],   # 设置输出字段
    )
    return result
    """
    同样的 distance 字段, 如果是 IP(内积),那就是越大越好, 
    L2(欧氏距离)	    向量间的直线距离	  越小越好	    升序(距离小的在前)
    IP(内积)	       向量点积	            越大越好	  降序(内积大的在前)
    COSINE(余弦相似度)  向量夹角的余弦值	   越大越好	     降序(相似度大的在前)
    HAMMING(汉明距离)   二进制向量不同位个数   越小越好	     升序
    JACCARD(杰卡德距离)	集合差异度	          越小越好	    升序
    """

# 混合检索

if __name__ == "__main__":
    milvus_client = get_milvus_client()
    # results = search_dense_vector(
    #     milvus_client=milvus_client,
    #     collection_name='demo',
    #     query='极大似然'
    # )

    results = search_sparse_vector(
        milvus_client=milvus_client,
        collection_name='demo',
        query='极大似然'
    )
    rprint(results)
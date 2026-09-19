"""
    测试 Milvus 进行向量检索
"""
import numpy as np
from pymilvus import AnnSearchRequest, MilvusClient, RRFRanker
from FlagEmbedding import BGEM3FlagModel
from rich import print as rprint
from common import deepseek

# 创建 Milvus 客户端对象
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")

# 将用户的问题转换为向量
def embed_query(query: str):
    bge_model = BGEM3FlagModel(model_name_or_path="/Users/refone/Coding/ai/bge-m3")
    result = bge_model.encode([query],
                              return_dense=True,
                              return_sparse=True,
                              )
    # FlagEmbedding 在本机以半精度加载模型, dense_vecs 是 float16,
    # 而集合中 dense_vector 字段是 float32, 必须转换, 否则检索时向量类型不匹配
    dense_vector = np.array(result["dense_vecs"], dtype=np.float32)
    # FlagEmbedding 2.x 的 lexical_weights 键是字符串、值是 float16,
    # Milvus 稀疏向量要求 {int: float}, 统一转换
    sparse_vector = [
        {int(token_id): float(weight) for token_id, weight in lw.items()}
        for lw in result["lexical_weights"]
    ]
    return dense_vector, sparse_vector

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
    # 获取 query 所对应的稀疏向量
    _, sparse_vector = embed_query(query)
    # 进行稀疏向量检索
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
def search_hybrid(milvus_client: MilvusClient, collection_name: str, query: str, limit: int):
    # 获取 query 所对应的稠密向量
    dense_vector, sparse_vector = embed_query(query)

    # 稠密向量的检索方式
    req_dense = AnnSearchRequest(
        data=dense_vector,          # 要检索的向量, 已是 (1, dim) 的二维数组, 不能再套一层列表
        anns_field="dense_vector",  # 要进行相似度比较的字段
        param={"metric_type":"L2"}, # 比较相似度的方式
        limit=limit,
    )

    # 稀疏向量的检索方式
    req_sparse = AnnSearchRequest(
        data=sparse_vector,         # 要检索的向量, 已是元素为 {token_id: weight} 字典的一维数组
        anns_field="sparse_vector", # 要进行相似度比较的字段
        param={"metric_type":"IP"}, # 比较相似度的方式
        limit=limit,
    )

    # 进行混合检索
    result = milvus_client.hybrid_search(
        collection_name=collection_name,    # 集合名称
        reqs=[req_dense, req_sparse],       # 稠密向量和稀疏向量的检索方式
        ranker=RRFRanker(k=60),             # 重排序规则(倒数融合排序)
        limit=limit,
        output_fields=["id", "text", "metadata"]
    )

    return result

def llm_query(llm, query: str):
    milvus_client = get_milvus_client()
    # 通过混合检索获取结果
    chunks = search_hybrid(
        milvus_client=milvus_client,
        collection_name="demo",
        query=query,
        limit=3,
    )

    # 对检索结果进行处理, 将检索到的数据片段转换为字符串
    context = "\n".join([ chunk["entity"]["text"] for chunk in chunks[0] ])

    return llm.invoke(
        [
            {"role": "system", "content": "你是一个专业的法律问答机器人，请根据上下文回答问题，当上下文无法回答问题时，请回答“根据上下文无法回答该问题”"},
            {"role": "user", "content": f"根据以下上下文回答问题：{context}\n问题：{query}"}
        ]
    )

if __name__ == "__main__":
    milvus_client = get_milvus_client()

    # dv, sv = embed_query("极大似然")
    # rprint(dv, sv)

    # results = search_dense_vector(
    #     milvus_client=milvus_client,
    #     collection_name='demo',
    #     query='极大似然'
    # )
    # rprint(results)

    # results = search_sparse_vector(
    #     milvus_client=milvus_client,
    #     collection_name='demo',
    #     query='极大似然'
    # )
    # rprint(results)

    # results = search_hybrid(
    #     milvus_client=milvus_client,
    #     collection_name='demo',
    #     query='极大似然',
    #     limit=3,
    # )
    # rprint(results)

    results = llm_query(deepseek, "极大似然")
    rprint(results)

"""
    测试: milvus 删除实体和标量检索
"""
from pymilvus import MilvusClient
from rich import print as rprint

# 创建 Milvus 客户端对象
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")

def delete_data(milvus_client: MilvusClient, collection_name: str):
    result = milvus_client.delete(
        collection_name=collection_name,
        # filter="id == ..."
        filter="id in [..., ...]"
    )
    print(result)

def search_data(
        milvus_client: MilvusClient,
        collection_name: str,
        keyword: str
        ):
    result = milvus_client.query(
        filter=f"text like '%{keyword}%'",
        output_fields=["id", "text"],
    )

    return result

if __name__ == "__main__":
    milvus_client = get_milvus_client()
    # delete_data(milvus_client, collection_name="demo")

    result = search_data(milvus_client, "demo", keyword="极大似然")
    rprint(result)
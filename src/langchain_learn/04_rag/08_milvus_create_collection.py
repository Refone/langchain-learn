"""
    测试: 创建 Milvus 集合
"""
from pymilvus import DataType, MilvusClient

# 创建 Milvus 客户端对象
def get_milvus_client():
    return MilvusClient(uri="http://localhost:19530")

# 获取 Milvus 中所有的集合
def find_all_collection(milvus_client: MilvusClient):
    print(milvus_client.list_collections)

# 创建集合
def milvus_create_collection(
        milvus_client: MilvusClient,
        collection_name: str):

    if not milvus_client.has_collection(collection_name):
        # 若没有该集合, 则创建

        # 首先设置集合结构
        schema = milvus_client.create_schema(
            auto_id = True,     # 设置当前集合自动生成 id (主键)
        )
        # id_primary_True: 将该字段设置为主键,
        # 若创建结构对象时, 设置了 auto_id = True,
        # 则添加数据时不需要为主键赋值,会自动生成
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
        schema.add_field(field_name="metadata", datatype=DataType.JSON)
        schema.add_field(field_name="dense_vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
        schema.add_field(field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR)

        # 然后设置索引
        index_params = milvus_client.prepare_index_params()
        index_params.add_index(
            field_name="dense_vector",          # 设置创建索引的字段名
            index_name="dense_vector_index",    # 自定义索引名称, 不设置会自动生成
            index_type="HNSW",                  # 设置索引类型
            metric_type="L2",                   # 计算相似度的方式 L2 | IP | cosine
        )
        index_params.add_index(
            field_name="sparse_vector",
            index_name="sparse_vector_index",
            index_type="SPARSE_INVERTED_INDEX",
            metric_type="IP",
        )

        milvus_client.create_collection(
            collection_name=collection_name,    # 集合名称
            schema=schema,
            index_params=index_params,
        )

if __name__ == "__main__":
    # 获取 Miluvus 的客户端连接
    milvus_client = get_milvus_client()

    # 创建名为 demo 的 collection
    milvus_create_collection(milvus_client, "demo")
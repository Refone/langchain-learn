"""
    测试: 使用 bge_m3 来生成稠密向量和稀疏向量
"""
from FlagEmbedding import BGEM3FlagModel
from rich import print as rprint

# 创建 bge_m3 模型对象
model = BGEM3FlagModel(
    model_name_or_path="/Users/refone/Coding/ai/bge-m3"
)

# 对数据进行向量化
# 将数据转换为稠密向量和稀疏向量
result = model.encode(
    sentences=[
        "标量字段通常用来存储一些元数据"
    ],                      # 设置需要转换的数据
    return_dense=True,      # 设置返回稠密向量
    return_sparse=True,     # 设置返回稀疏向量
)

# rprint(result)
"""
{
    'dense_vecs': array([[-0.02713 , -0.03687 , -0.0859  , ...,  0.004032, -0.01822 ,
        -0.01944 ]], shape=(1, 1024), dtype=float16),
    'lexical_weights': [
        defaultdict(<class 'int'>, {
            '6': np.float16(0.05457),
            '23204': np.float16(0.265),
            '3272': np.float16(0.2883),
            '7234': np.float16(0.1804),
            '12002': np.float16(0.267),
            '17072': np.float16(0.172),
            '140278': np.float16(0.1593),
            '165497': np.float16(0.2181),
            '4321': np.float16(0.0827),
            '2954': np.float16(0.2059),
            '12833': np.float16(0.2225)
        })
    ],
    'colbert_vecs': None
}
"""

dense_vector = result["dense_vecs"][0]
sparse_vector = result["lexical_weights"][0]

# 将稀疏向量进行反向解析,将索引转换为 token
rprint(model.convert_id_to_token(sparse_vector))
"""
{
    '': np.float16(0.05457),
    '标': np.float16(0.265),
    '量': np.float16(0.2883),
    '字': np.float16(0.1804),
    '段': np.float16(0.267),
    '通常': np.float16(0.172),
    '用来': np.float16(0.1593),
    '存储': np.float16(0.2181),
    '一些': np.float16(0.0827),
    '元': np.float16(0.2059),
    '数据': np.float16(0.2225)
}
"""


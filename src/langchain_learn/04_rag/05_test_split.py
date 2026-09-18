"""
    测试: 使用 RecursiveCharacterTextSplitter 进行文档分割
"""

from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich import print as rprint

# 读取文档中的内容
documents = UnstructuredWordDocumentLoader(
    file_path="/Users/refone/Desktop/math.docx",
    model="single",
).load()

# rprint(documents)

def get_length(chunk):
    return len(chunk)

# 创建递归切分对象
spliter = RecursiveCharacterTextSplitter(
    # 每一次用列表第一个字符进行切分, 如果结果超过指定长度,
    # 把文档中第一个分割符删掉, (\n\n删掉, 然后用第二个进行切分)
    # 直至满足长度限制
    separators=["\n\n", "\n", "。", "！", "？", "……", "，", ""],
    chunk_size=400,             # 每个切片的大小
    chunk_overlap=50,           # 设置重叠的字符数
    length_function=get_length, # 计算切片长度的函数
    add_start_index=True,       # 是否为每个切片添加 start_index 属性, 记录当前切片在整个文档中的起始索引
)

# 切分文档, 返回 List[Documents]
chunks = spliter.split_documents(documents=documents)

max_iter = 5
for chunk in chunks:
    max_iter -= 1
    print('iter ', "="*50)
    rprint(chunk)
    if max_iter < 0:
        break
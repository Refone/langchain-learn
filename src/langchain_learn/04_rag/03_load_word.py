"""
    测试：加载word文档
"""
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

# 创建文档加载器对象
loader = UnstructuredWordDocumentLoader(
    file_path="/Users/refone/Desktop/LangChainV1.1.0.docx",
)

# 加载文档
documents = loader.load()
print(documents[0])
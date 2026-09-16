"""
    测试：使用UnstructuredMarkdownLoader加载md文件
    选择的模式mode="single"，表示将整个文档的内容加载为一个Document对象
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader

# 创建UnstructuredMarkdownLoader对象
loader = UnstructuredMarkdownLoader(
    file_path="/Users/refone/Downloads/清华暑期培训/Lectures/2 Git与GitHub .md",
    mode="single"
)

# 加载文档
documents = loader.load()

print(documents[0].page_content)
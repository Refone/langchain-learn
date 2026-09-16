"""
    测试：使用UnstructuredMarkdownLoader加载md文件
    选择的模式mode="elements"，表示将整个文档的内容进行切分，每个数据片段都会加载为一个Document对象
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from rich import print as rprint

# 创建加载器对象
loader = UnstructuredMarkdownLoader(
    file_path="/Users/refone/Downloads/清华暑期培训/Lectures/2 Git与GitHub .md",
    mode="elements"
)

# 记载文档
documents = loader.load()
print(f"文档被切分为{len(documents)}个数据片段")
for document in documents:
    rprint(document)
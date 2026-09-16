"""
    使用 MinerU 将 pdf 文件转换为 md 文件
    在这个过程中需要发送三次请求:
    1. 第一次请求, MinerU 会返回一个 url, 提供该 url 上传 pdf 文件
    2. 第二次请求, 上传 pdf 文件
    3. 第三次请求, 获取最终结果(压缩文件的url地址,压缩文件中是 pdf 转换之后的 md 文件)
"""

# 设置请求需要的数据
# https://mineru.net/apiManage/docs

from pathlib import Path
from rich import print as rprint
from dotenv import load_dotenv

import requests
import os

load_dotenv(override=True)

token = os.getenv("MINERU_API")

def upload_pdf_mineru(path):
    # 1) 指定本地目录，自动收集该目录下所有 PDF
    folder = Path(path)
    folder_name = folder.name  # 目录名，用于生成 data_id

    file_paths = sorted(folder.glob("*.pdf"))  # 排序保证顺序稳定
    if not file_paths:
        raise FileNotFoundError(f"目录 {folder} 下没有找到 PDF 文件")

    # 2) 根据文件名生成 files 列表：name 用文件名，data_id 用 <目录名_序号>
    files = [
        {"name": p.name, "data_id": f"{folder_name}_{i}"}
        for i, p in enumerate(file_paths)
    ]

    url = "https://mineru.net/api/v4/file-urls/batch"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "files": files,
        "model_version": "vlm"
    }

    try:
        # 发送第一次请求
        response = requests.post(url, headers=header, json=data)
        # 判断响应状态码是非为 200
        if response.status_code == 200:
            # 表示请求成功, 获取服务器响应的结果
            result = response.json()
            # 判断结构状态码
            if result.get("code") == 0:
                # 成功
                # 分别获取任务的 batch_id 和上传 pdf 的 file_urls
                batch_id = result["data"]["batch_id"]
                urls = result["data"]["file_urls"]
                print('batch_id:{},urls:{}'.format(batch_id, urls))
                for i in range(0, len(urls)):
                    with open(file_paths[i], 'rb') as f:
                        # 发送第二次请求
                        res_upload = requests.put(urls[i], data=f)
                        if res_upload.status_code == 200:
                            print(f"{urls[i]} upload success")
                            return batch_id
                        else:
                            print(f"{urls[i]} upload failed")
            else:
                # 失败
                print(f"第一次请求接口调用失败, 接口状态码:{result.get('code')}, 状态码信息: {result.get('msg')}")
    except Exception as e:
        print(f"发送请求失败, {e}")

def get_mineru_result(batch_id):
    url = f"https://mineru.net/api/v4/extract-results/batch/{batch_id}"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(url, headers=header)
    return res.json()
    # print(res.status_code)
    # print(res.json())
    # print(res.json()["data"])

if __name__ == '__main__':
    # batch_id = upload_pdf_mineru('/Users/refone/Desktop/LangChain/docs')
    # res = get_mineru_result(batch_id)
    res = get_mineru_result("fb80109c-8186-4171-8d06-341f82968e56")

    # rprint(res.data.extract_result.full_zip_url)
    rprint(res["data"]["extract_result"][0]["full_zip_url"])
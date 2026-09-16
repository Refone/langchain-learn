"""
    使用 MinerU 将 pdf 文件转换为 md 文件
    在这个过程中需要发送三次请求:
    1. 第一次请求, MinerU 会返回一个 url, 提供该 url 上传 pdf 文件
    2. 第二次请求, 上传 pdf 文件
    3. 第三次请求, 获取最终结果(压缩文件的url地址,压缩文件中是 pdf 转换之后的 md 文件)
"""

# 设置请求需要的数据
# https://mineru.net/apiManage/docs
from dotenv import load_dotenv

import os
import requests

load_dotenv(override=True)

token = os.getenv("MINERU_API")

def upload_pdf_mineru():
    url = "https://mineru.net/api/v4/file-urls/batch"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "files": [
            {"name":"sample.pdf", "data_id": "test-01"}
        ],
        "model_version":"vlm"
    }

    file_path = ["/Users/refone/Coding/ai/langchain-learn/src/rag/assets/sample.pdf"]

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
                    with open(file_path[i], 'rb') as f:
                        # 发送第二次请求
                        res_upload = requests.put(urls[i], data=f)
                        if res_upload.status_code == 200:
                            print(f"{urls[i]} upload success")
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
    print(res.status_code)
    print(res.json())
    print(res.json()["data"])

if __name__ == '__main__':
    get_mineru_result("9e8b9a29-9e44-4890-98fe-9d88ba464e01")
    # result:
    # {
    #   'batch_id': '9e8b9a29-9e44-4890-98fe-9d88ba464e01', 
    #   'extract_result': [{
    #       'data_id': 'test-01', 
    #       'file_name':'sample.pdf', 
    #       'state': 'done', 
    #       'err_msg': '', 
    #       'full_zip_url': 'https://cdn-mineru.openxlab.org.cn/pdf/2026-07-29/742987ce-b081-4f62-9386-2b7ba5d2078a.zip'}
    #    ]}
from dotenv import load_dotenv
import os
from pydantic import BaseModel
# Load environment variables from .env file
load_dotenv()
from openai import OpenAI

# Retrieve the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.duckagi.com/v1/")

def openai_wrapper(system_messages,input_messages,response_format):
    system_messages = {"role": "system", "content": f"{system_messages}"}
    input_messages = {"role": "user", "content": f"{input_messages}"}
    
    messages = [system_messages]
    messages.append(input_messages)
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=response_format,
    )
    completion_result = completion.choices[0].message

    if completion_result.parsed:
        result = completion_result.parsed
        return result
    else:
        print(completion_result.refusal)


import requests

def jinahtml2string(html):
    api_key = os.getenv("JINA_API_KEY")
    url = f"https://r.jina.ai/{html}"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        return response.text  # Return the response content as string
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

from bs4 import BeautifulSoup

import requests

def extract_core_content(url):
    """
    使用 beautifulsoup 去对一个网页进行解析，尝试去得到一些对应的结果，
    我只希望提取这里面的核心内容
    """
    # 发送HTTP请求来加载url内容
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 假设核心内容在 <div> 标签中，可以根据具体情况修改
    core_content = soup.find_all('div')
    

    # todo 使用一个相似度函数去对这里的文本进行打分，从而可以降低对于token的需求，至少不需要是查找一个数据都需要上前也
    if core_content:
        return [div.get_text(strip=True) for div in core_content]
    else:
        return []


if __name__ == "__main__":
    html = "https://en.wikipedia.org/wiki/Lionel_Messi"
    bs_result = extract_core_content(html)
    print(len(bs_result))
    # print(bs_result)
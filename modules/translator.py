# -*- coding: utf-8 -*-
import requests
import json
from config import DEEPSEEK_API_KEY

class Translator:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def translate(self, text):
        print(f"正在翻译文本: {text}")
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": f"Translate the following Japanese text to Chinese:\n{text}\nOnly return the translated text, no other words."
                }
            ],
            "temperature": 0.1,
            "max_tokens": 2000
        }
        
        try:
            with requests.Session() as session:
                response = session.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers=self.headers,
                    json=data,
                    timeout=10
                )
            
            if response.status_code != 200:
                error_msg = f"API 请求失败: HTTP {response.status_code}"
                print(error_msg)
                return error_msg
                
            try:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    translated = result['choices'][0]['message']['content']
                    print(f"翻译结果: {translated}")
                    return translated
                else:
                    error_msg = "API 响应格式错误"
                    print(error_msg)
                    return error_msg
            except json.JSONDecodeError as e:
                error_msg = f"JSON 解析错误: {str(e)}"
                print(error_msg)
                return error_msg
                
        except requests.exceptions.Timeout:
            return "翻译请求超时"
        except requests.exceptions.RequestException as e:
            return f"网络请求错误: {str(e)}"
        except Exception as e:
            return f"翻译出错: {str(e)}" 
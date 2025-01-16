# -*- coding: utf-8 -*-
import re

class TextProcessor:
    @staticmethod
    def clean_japanese_text(text):
        # 移除单个英文字母和数字
        text = re.sub(r'(?<![A-Za-z])[A-Za-z](?![A-Za-z])', '', text)
        text = re.sub(r'(?<!\d)\d(?!\d)', '', text)
        
        # 保留日文字符、标点符号和空格
        text = re.sub(r'[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3000-\u303F\s]', '', text)
        
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    @staticmethod
    def post_process_text(text):
        if not text:
            return text
            
        # 移除所有非日文字符
        text = re.sub(r'[a-zA-Z0-9]', '', text)
        
        # 移除可能的OCR错误
        text = re.sub(r'([。、！？…―])\1+', r'\1', text)
        
        # 确保日文句子的正确性
        text = re.sub(r'([。、！？])(?=[^\s])', r'\1\n', text)
        
        # 处理行
        lines = text.split('\n')
        processed_lines = []
        for line in lines:
            line = re.sub(r'^[^。、！？…―「」『』（）［］【】《》〈〉｛｝〔〕・：\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+', '', line)
            line = re.sub(r'[^。、！？…―「」『』（）［］【】《》〈〉｛｝〔〕・：\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+$', '', line)
            if line.strip():
                processed_lines.append(line.strip())
        
        text = '\n'.join(processed_lines)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        
        return text.strip() 
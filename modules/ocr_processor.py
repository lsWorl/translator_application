# -*- coding: utf-8 -*-
import pytesseract
from .text_processor import TextProcessor
from config import TESSERACT_CMD, OCR_CONFIGS

# 设置Tesseract-OCR路径
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

class OCRProcessor:
    def __init__(self):
        self.configs = OCR_CONFIGS
    
    def recognize_text(self, image):
        best_text = ''
        best_length = 0
        best_config = ''
        
        for config in self.configs:
            try:
                text = pytesseract.image_to_string(
                    image,
                    lang='jpn+jpn_vert',
                    config=config['config']
                )
                cleaned_text = TextProcessor.clean_japanese_text(text)
                if len(cleaned_text) > best_length:
                    best_length = len(cleaned_text)
                    best_text = cleaned_text
                    best_config = config['name']
                print(f"OCR结果 ({config['name']}): {text}")
            except Exception as e:
                print(f"OCR错误 ({config['name']}): {str(e)}")
        
        if best_text.strip():
            print(f"最佳识别结果 ({best_config}): {best_text}")
        
        return best_text 
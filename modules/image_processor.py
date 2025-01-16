# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image
from datetime import datetime
from config import (
    IMAGE_SCALE,
    CLAHE_CLIP_LIMIT,
    CLAHE_GRID_SIZE,
    BILATERAL_FILTER_PARAMS,
    ADAPTIVE_THRESHOLD_BLOCK_SIZE,
    ADAPTIVE_THRESHOLD_C,
    MORPH_KERNEL_SIZE
)

class ImageProcessor:
    @staticmethod
    def preprocess_image(image):
        # 转换为灰度图
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        
        # 放大图像
        width = int(gray.shape[1] * IMAGE_SCALE)
        height = int(gray.shape[0] * IMAGE_SCALE)
        gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LANCZOS4)
        
        # 对比度增强
        clahe = cv2.createCLAHE(clipLimit=CLAHE_CLIP_LIMIT, tileGridSize=CLAHE_GRID_SIZE)
        gray = clahe.apply(gray)
        
        # 双边滤波减少噪声同时保留边缘
        gray = cv2.bilateralFilter(
            gray,
            d=BILATERAL_FILTER_PARAMS['d'],
            sigmaColor=BILATERAL_FILTER_PARAMS['sigma_color'],
            sigmaSpace=BILATERAL_FILTER_PARAMS['sigma_space']
        )
        
        # 自适应阈值二值化
        binary = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            ADAPTIVE_THRESHOLD_BLOCK_SIZE,
            ADAPTIVE_THRESHOLD_C
        )
        
        # 形态学操作
        kernel = np.ones(MORPH_KERNEL_SIZE, np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        return Image.fromarray(binary)
    
    @staticmethod
    def save_debug_image(image, prefix, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{prefix}_{timestamp}.png"
        image.save(filename)
        print(f"已保存图像: {filename}")
        return filename 
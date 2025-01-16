# -*- coding: utf-8 -*-

# Tesseract-OCR配置
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 修改为你的Tesseract-OCR路径

# DeepSeek API配置
DEEPSEEK_API_KEY = 'your-api-key-here'  # 替换为你的DeepSeek API密钥

# OCR配置
OCR_CONFIGS = [
    {'config': '--oem 1 --psm 6 -l jpn+jpn_vert', 'name': '标准模式'},
    {'config': '--oem 1 --psm 7 -l jpn+jpn_vert', 'name': '单行模式'},
    {'config': '--oem 1 --psm 11 -l jpn+jpn_vert', 'name': '稀疏文本模式'},
    {'config': '--oem 1 --psm 3 -l jpn+jpn_vert', 'name': '原始模式'}
]

# 图像处理配置
IMAGE_SCALE = 4.0  # 图像缩放比例
CLAHE_CLIP_LIMIT = 3.5  # CLAHE对比度限制
CLAHE_GRID_SIZE = (8, 8)  # CLAHE网格大小
BILATERAL_FILTER_PARAMS = {
    'd': 9,
    'sigma_color': 75,
    'sigma_space': 75
}
ADAPTIVE_THRESHOLD_BLOCK_SIZE = 11
ADAPTIVE_THRESHOLD_C = 2
MORPH_KERNEL_SIZE = (2, 2)

# UI配置
WINDOW_TITLE = '日语实时翻译器 [置顶模式]'
WINDOW_SIZE = (800, 600)
WINDOW_POS = (100, 100)
CHECK_INTERVAL = 500  # 毫秒
MIN_SELECTION_SIZE = 10  # 最小选择区域大小 
# -*- coding: utf-8 -*-
import sys
import os
import time
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QWidget, QLabel, 
                           QTextEdit, QMessageBox, QCheckBox, QComboBox)
from PyQt5.QtCore import Qt, QTimer
from PIL import ImageGrab
import win32gui

from modules import (
    ImageProcessor,
    OCRProcessor,
    TextProcessor,
    Translator,
    WindowManager,
    ScreenshotOverlay
)
from config import (
    WINDOW_TITLE,
    WINDOW_SIZE,
    WINDOW_POS,
    CHECK_INTERVAL,
    MIN_SELECTION_SIZE
)

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # 初始化模块
        self.image_processor = ImageProcessor()
        self.ocr_processor = OCRProcessor()
        self.text_processor = TextProcessor()
        self.translator = Translator()
        self.window_manager = WindowManager()
        
        # 初始化变量
        self.init_variables()
        
        # 初始化UI
        self.init_ui()
        
        # 设置定时器
        self.setup_timer()
        
        # 创建截图目录
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        print("翻译器应用已启动")
    
    def init_variables(self):
        self.monitor_area = None
        self.last_text = ""
        self.last_check_time = time.time()
        self.check_interval = CHECK_INTERVAL / 1000  # 转换为秒
        self.screenshot_count = 0
        self.overlay = None
        self.is_processing_enabled = True
        self.target_window_hwnd = None
        self.last_window_rect = None
        self.consecutive_empty_count = 0
    
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_screen_content)
        self.timer.start(CHECK_INTERVAL)
    
    def init_ui(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(WINDOW_POS[0], WINDOW_POS[1], WINDOW_SIZE[0], WINDOW_SIZE[1])
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加控制区域
        control_layout = self.create_control_layout()
        layout.addLayout(control_layout)
        
        # 添加文本显示区域
        text_layout = self.create_text_layout()
        layout.addLayout(text_layout)
    
    def create_control_layout(self):
        control_layout = QHBoxLayout()
        
        # 窗口选择区域
        window_select_layout = QHBoxLayout()
        window_select_label = QLabel('选择目标窗口:', self)
        window_select_layout.addWidget(window_select_label)
        
        self.window_combo = QComboBox(self)
        self.window_combo.setMinimumWidth(200)
        self.refresh_window_list()
        window_select_layout.addWidget(self.window_combo)
        
        self.refresh_btn = QPushButton('刷新窗口列表', self)
        self.refresh_btn.clicked.connect(self.refresh_window_list)
        window_select_layout.addWidget(self.refresh_btn)
        
        control_layout.addLayout(window_select_layout)
        
        # 其他控制按钮
        self.select_area_btn = QPushButton('选择翻译区域', self)
        self.select_area_btn.clicked.connect(self.start_screenshot)
        control_layout.addWidget(self.select_area_btn)
        
        self.process_checkbox = QCheckBox('启用图像预处理', self)
        self.process_checkbox.setChecked(True)
        self.process_checkbox.stateChanged.connect(self.toggle_processing)
        control_layout.addWidget(self.process_checkbox)
        
        self.clear_btn = QPushButton('清除文本', self)
        self.clear_btn.clicked.connect(self.clear_text)
        control_layout.addWidget(self.clear_btn)
        
        return control_layout
    
    def create_text_layout(self):
        text_layout = QHBoxLayout()
        
        # 原文区域
        original_layout = QVBoxLayout()
        original_label = QLabel('原文:', self)
        original_layout.addWidget(original_label)
        self.original_text = QTextEdit(self)
        self.original_text.setPlaceholderText('原文')
        self.original_text.setReadOnly(True)
        original_layout.addWidget(self.original_text)
        text_layout.addLayout(original_layout)
        
        # 译文区域
        translated_layout = QVBoxLayout()
        translated_label = QLabel('译文:', self)
        translated_layout.addWidget(translated_label)
        self.translated_text = QTextEdit(self)
        self.translated_text.setPlaceholderText('译文')
        self.translated_text.setReadOnly(True)
        translated_layout.addWidget(self.translated_text)
        text_layout.addLayout(translated_layout)
        
        return text_layout
    
    def refresh_window_list(self):
        self.window_combo.clear()
        self.windows = self.window_manager.get_window_list()
        for title, _ in self.windows:
            self.window_combo.addItem(title)
        print("窗口列表已刷新")
    
    def start_screenshot(self):
        current_index = self.window_combo.currentIndex()
        if current_index < 0:
            QMessageBox.warning(self, "警告", "请先选择一个目标窗口")
            return
            
        _, hwnd = self.windows[current_index]
        self.target_window_hwnd = hwnd
        
        if not self.window_manager.activate_window(hwnd):
            QMessageBox.warning(self, "警告", "无法激活选中的窗口")
            return
        
        time.sleep(0.2)
        print("开始截图流程")
        self.hide()
        self.overlay = ScreenshotOverlay(callback=self.handle_screenshot_result)
        QTimer.singleShot(100, self._show_overlay)
    
    def _show_overlay(self):
        if self.overlay:
            self.overlay.show()
            self.overlay.activateWindow()
            self.overlay.raise_()
            print("显示截图窗口")
    
    def handle_screenshot_result(self, area):
        if area:
            x1, y1, x2, y2 = area
            print(f"处理截图结果: ({x1}, {y1}) -> ({x2}, {y2})")
            window_rect = self.window_manager.get_window_rect(self.target_window_hwnd)
            if window_rect:
                window_x, window_y, _, _ = window_rect
                rel_x1 = x1 - window_x
                rel_y1 = y1 - window_y
                rel_x2 = x2 - window_x
                rel_y2 = y2 - window_y
                self.set_monitor_area(rel_x1, rel_y1, rel_x2, rel_y2)
                print(f"设置相对坐标: ({rel_x1}, {rel_y1}) -> ({rel_x2}, {rel_y2})")
            else:
                print("无法获取窗口位置")
        self.show()
        self.activateWindow()
    
    def set_monitor_area(self, x1, y1, x2, y2):
        self.monitor_area = (x1, y1, x2, y2)
        print(f"设置监控区域: {self.monitor_area}")
        QTimer.singleShot(500, self.check_screen_content)
        self.show()
    
    def check_screen_content(self):
        if not self.monitor_area or not self.target_window_hwnd:
            return
            
        try:
            if not win32gui.IsWindow(self.target_window_hwnd):
                print("目标窗口已关闭")
                self.monitor_area = None
                self.target_window_hwnd = None
                return
                
            window_rect = self.window_manager.get_window_rect(self.target_window_hwnd)
            if not window_rect:
                print("无法获取窗口位置")
                return
                
            x1, y1, x2, y2 = self.monitor_area
            window_x, window_y, _, _ = window_rect
            
            screen_x1 = window_x + x1
            screen_y1 = window_y + y1
            screen_x2 = window_x + x2
            screen_y2 = window_y + y2
            
            print(f"当前截图区域: ({screen_x1}, {screen_y1}) -> ({screen_x2}, {screen_y2})")
            
            screenshot = ImageGrab.grab(bbox=(screen_x1, screen_y1, screen_x2, screen_y2))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 保存原始截图
            self.image_processor.save_debug_image(screenshot, "original", timestamp)
            
            if self.is_processing_enabled:
                processed_image = self.image_processor.preprocess_image(screenshot)
                self.image_processor.save_debug_image(processed_image, "processed", timestamp)
            else:
                processed_image = screenshot
            
            # OCR识别
            best_text = self.ocr_processor.recognize_text(processed_image)
            
            if best_text.strip():
                # 应用额外的文本后处理
                post_processed_text = TextProcessor.post_process_text(best_text)
                
                if post_processed_text != self.last_text:
                    print(f"检测到新文本: {post_processed_text}")
                    self.last_text = post_processed_text
                    self.original_text.setText(post_processed_text)
                    translated = self.translator.translate(post_processed_text)
                    self.translated_text.setText(translated)
            else:
                print("未检测到有效文本")
                
        except Exception as e:
            print(f"检查屏幕内容时出错: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def toggle_processing(self, state):
        self.is_processing_enabled = state == Qt.Checked
        print(f"图像预处理已{'启用' if self.is_processing_enabled else '禁用'}")
    
    def clear_text(self):
        self.original_text.clear()
        self.translated_text.clear()
        self.last_text = ""
        print("已清除文本")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec_()) 
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen

class ScreenshotOverlay(QWidget):
    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.callback = callback
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
        self.init_variables()
        print("截图窗口已创建")
    
    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 100);
            }
            QLabel {
                color: white;
                background-color: transparent;
                font-size: 16px;
            }
        """)
        
        self.hint_label = QLabel("按住鼠标左键并拖动选择翻译区域\n按ESC取消选择", self)
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setStyleSheet("background-color: rgba(0, 0, 0, 150); padding: 10px;")
        
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        self.setGeometry(screen.geometry())
        
        self.update_hint_label_position()
    
    def init_variables(self):
        self.begin = QPoint()
        self.end = QPoint()
        self.is_drawing = False
    
    def update_hint_label_position(self):
        self.hint_label.setGeometry(
            (self.width() - 300) // 2,
            (self.height() - 60) // 2,
            300,
            60
        )
    
    def showEvent(self, event):
        super().showEvent(event)
        self.activateWindow()
        print("截图窗口显示")
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        if self.is_drawing:
            pen = QPen(QColor(0, 174, 255), 2)
            painter.setPen(pen)
            rect = QRect(self.begin, self.end)
            painter.drawRect(rect)
            painter.fillRect(rect, QColor(0, 0, 0, 0))
            size_text = f"{abs(self.end.x() - self.begin.x())} × {abs(self.end.y() - self.begin.y())}"
            painter.drawText(rect.center(), size_text)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            print("用户取消选择")
            self.callback(None)
            self.close()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = self.begin
            self.is_drawing = True
            self.hint_label.hide()
            print(f"开始截图: 起始点 ({self.begin.x()}, {self.begin.y()})")
    
    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.end = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_drawing:
            self.is_drawing = False
            print(f"结束截图: 终点 ({self.end.x()}, {self.end.y()})")
            self.capture_area()
            self.close()
    
    def capture_area(self):
        if self.begin and self.end:
            x1, y1 = min(self.begin.x(), self.end.x()), min(self.begin.y(), self.end.y())
            x2, y2 = max(self.begin.x(), self.end.x()), max(self.begin.y(), self.end.y())
            
            if x2 - x1 > 10 and y2 - y1 > 10:
                print(f"截图区域: ({x1}, {y1}) -> ({x2}, {y2})")
                self.callback((x1, y1, x2, y2))
            else:
                print("选区太小")
                QMessageBox.warning(self, "警告", "请选择更大的区域（至少10×10像素）")
                self.callback(None) 
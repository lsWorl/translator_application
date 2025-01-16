# -*- coding: utf-8 -*-
import win32gui

class WindowManager:
    @staticmethod
    def get_window_list():
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title and not title.startswith("翻译器"):
                    windows.append((title, hwnd))
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows
    
    @staticmethod
    def get_window_rect(hwnd):
        try:
            return win32gui.GetWindowRect(hwnd)
        except:
            return None
    
    @staticmethod
    def activate_window(hwnd):
        try:
            win32gui.SetForegroundWindow(hwnd)
            return True
        except:
            return False 
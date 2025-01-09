from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QSystemTrayIcon, QMenu, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer, QSettings
from PyQt6.QtGui import QColor, QScreen, QPixmap, QIcon, QAction
import numpy as np
from PIL import ImageGrab

from ui.screenshot_overlay import ScreenshotOverlay
from utils.icon_manager import create_icon
from ocr.paddle_ocr import OCRProcessor

class ScreenshotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建 QSettings 对象
        self.settings = QSettings('OCRTool', 'ScreenshotApp')
        self.initUI()
        self.begin = QPoint()
        self.end = QPoint()
        self.is_drawing = False
        self.ocr = OCRProcessor()
        self.setup_tray()
        self.setup_hotkey()
        # 设置窗口图标
        self.setWindowIcon(create_icon())
        # 防止重复触发
        self.is_capturing = False
        # 存储当前截图
        self.current_screenshot = None
        # 恢复窗口位置
        self.restore_window_position()

    # ... [其余方法保持不变，从原main.py复制] ... 
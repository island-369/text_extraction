from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QScreen, QApplication

class ScreenshotOverlay(QWidget):
    finished = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()
        # 捕获整个屏幕
        screen = QApplication.primaryScreen()
        self.original_pixmap = screen.grabWindow(0)
        self.initUI()
        self.begin = QPoint()
        self.end = QPoint()
        self.is_drawing = False

    # ... [其余方法保持不变，从原main.py复制] ... 
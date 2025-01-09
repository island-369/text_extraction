import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QScreen, QPixmap
import numpy as np
from PIL import ImageGrab
from paddleocr import PaddleOCR

class ScreenshotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.begin = QPoint()
        self.end = QPoint()
        self.is_drawing = False
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)

    def initUI(self):
        self.setWindowTitle('截图OCR工具')
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.capture_btn = QPushButton('开始截图', self)
        self.capture_btn.clicked.connect(self.start_capture)
        layout.addWidget(self.capture_btn)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText('识别结果将显示在这里...')
        layout.addWidget(self.text_edit)

    def start_capture(self):
        self.hide()
        # 等待一下让主窗口完全隐藏
        QApplication.processEvents()
        self.screen = ScreenshotOverlay()
        self.screen.finished.connect(self.process_screenshot)
        self.screen.show()

    def process_screenshot(self, geometry):
        # 立即显示主窗口并显示正在处理的提示
        self.show()
        self.text_edit.setText('正在识别中...')
        QApplication.processEvents()  # 立即更新界面

        if geometry.width() > 0 and geometry.height() > 0:
            # 确保坐标为正数
            x1, y1 = min(geometry.x(), geometry.x() + geometry.width()), min(geometry.y(), geometry.y() + geometry.height())
            x2, y2 = max(geometry.x(), geometry.x() + geometry.width()), max(geometry.y(), geometry.y() + geometry.height())
            
            try:
                screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                # 进行OCR识别
                result = self.ocr.ocr(np.array(screenshot))
                
                # 提取识别文本
                if result[0]:
                    text = '\n'.join([line[1][0] for line in result[0]])
                    self.text_edit.setText(text)
                else:
                    self.text_edit.setText('未能识别到文字')
            except Exception as e:
                self.text_edit.setText(f'截图失败: {str(e)}')

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

    def initUI(self):
        screen = QApplication.primaryScreen()
        geometry = screen.geometry()
        self.setGeometry(geometry)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setCursor(Qt.CursorShape.CrossCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 绘制原始屏幕图像
        painter.drawPixmap(self.rect(), self.original_pixmap)
        
        # 创建半透明遮罩
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        if self.is_drawing:
            # 恢复选择区域的原始图像
            select_rect = QRect(self.begin, self.end).normalized()
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
            painter.drawPixmap(select_rect, self.original_pixmap, select_rect)
            
            # 绘制红色边框
            pen = painter.pen()
            pen.setColor(QColor(255, 0, 0))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawRect(select_rect)

    def mousePressEvent(self, event):
        self.begin = event.position().toPoint()
        self.end = self.begin
        self.is_drawing = True
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.position().toPoint()
        self.update()

    def mouseReleaseEvent(self, event):
        if self.begin and self.end:
            self.hide()
            QApplication.processEvents()
            self.finished.emit(QRect(self.begin, self.end).normalized())
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScreenshotWindow()
    window.show()
    sys.exit(app.exec()) 
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QScreen

class ScreenshotOverlay(QWidget):
    # 自定义信号，当截图完成时发出
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
        """初始化UI"""
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen()
        geometry = screen.geometry()
        self.setGeometry(geometry)
        
        # 设置窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |  # 无边框
            Qt.WindowType.WindowStaysOnTopHint |  # 置顶
            Qt.WindowType.Tool  # 工具窗口
        )
        # 设置窗口状态
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        # 设置鼠标样式为十字
        self.setCursor(Qt.CursorShape.CrossCursor)
        # 设置提示文本
        self.help_text = "按住左键拖动选择区域，右键/ESC返回"
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        
        # 绘制原始屏幕图像
        painter.drawPixmap(self.rect(), self.original_pixmap)
        
        # 创建半透明遮罩
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        if self.is_drawing:
            # 恢复选择区域的原始图像
            select_rect = self.get_rect()
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
            painter.drawPixmap(select_rect, self.original_pixmap, select_rect)
            
            # 绘制边框
            pen = QPen(QColor(0, 120, 212), 2)  # 蓝色边框
            painter.setPen(pen)
            painter.drawRect(select_rect)
            
            # 显示尺寸信息
            size_text = f"{select_rect.width()} x {select_rect.height()}"
            painter.setPen(QColor(255, 255, 255))  # 白色文字
            painter.drawText(select_rect.right() + 5, select_rect.top() + 20, size_text)
        else:
            # 显示提示文本
            painter.setPen(QColor(255, 255, 255))
            font = painter.font()
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(10, 20, self.help_text)
    
    def get_rect(self):
        """获取选择区域的矩形"""
        return QRect(
            min(self.begin.x(), self.end.x()),
            min(self.begin.y(), self.end.y()),
            abs(self.end.x() - self.begin.x()),
            abs(self.end.y() - self.begin.y())
        )
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.begin = event.pos()
            self.end = self.begin
            self.is_drawing = True
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            # 右键取消
            self.hide()
            QApplication.processEvents()
            self.finished.emit(QRect())
            self.close()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.is_drawing:
            self.end = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_drawing:
            if self.begin and self.end and (self.begin != self.end):
                self.hide()
                QApplication.processEvents()
                self.finished.emit(self.get_rect())
                self.close()
            else:
                # 如果没有实际选择区域，保持截图界面
                self.is_drawing = False
                self.update()
    
    def keyPressEvent(self, event):
        """按键事件"""
        if event.key() == Qt.Key.Key_Escape:
            # ESC键取消
            self.hide()
            QApplication.processEvents()
            self.finished.emit(QRect())
            self.close() 
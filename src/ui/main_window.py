from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QSystemTrayIcon, QMenu, QHBoxLayout, QLabel, QApplication
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer, QSettings
from PyQt6.QtGui import QColor, QScreen, QPixmap, QIcon, QAction, QImage, QPainter, QKeySequence, QShortcut
import numpy as np
from PIL import ImageGrab, Image
from keyboard import add_hotkey, remove_hotkey

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
        self.setup_shortcuts()  # 添加快捷键设置
        # 设置窗口图标
        self.setWindowIcon(create_icon())
        # 防止重复触发
        self.is_capturing = False
        # 存储当前截图
        self.current_screenshot = None
        # 恢复窗口位置
        self.restore_window_position()

    def initUI(self):
        self.setWindowTitle('截图OCR工具')
        # 设置最小窗口大小，防止过度缩小导致布局混乱
        self.setMinimumSize(800, 600)
        
        # 如果是第一次运行，使用默认大小和位置
        if not self.settings.contains('geometry'):
            self.resize(1200, 800)  # 默认大小
            self.center()
        else:
            # 恢复上次的位置和大小
            self.restore_window_position()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)  # 设置布局间距
        layout.setContentsMargins(10, 10, 10, 10)  # 设置边距

        # 顶部按钮布局
        button_layout = QHBoxLayout()
        
        # 截图按钮
        self.capture_btn = QPushButton('开始截图 (Alt+C)', self)
        self.capture_btn.setFixedHeight(30)  # 设置按钮高度
        self.capture_btn.clicked.connect(self.start_capture)
        self.capture_btn.setStyleSheet('''
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
        ''')
        button_layout.addWidget(self.capture_btn)
        
        # 添加一些间距
        button_layout.addSpacing(10)
        
        # 重置按钮
        self.reset_btn = QPushButton('重置窗口', self)
        self.reset_btn.setFixedHeight(30)
        self.reset_btn.clicked.connect(self.reset_size)
        self.reset_btn.setStyleSheet('''
            QPushButton {
                background-color: #E0E0E0;
                border: none;
                border-radius: 4px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #D0D0D0;
            }
        ''')
        button_layout.addWidget(self.reset_btn)

        # 添加一些间距
        button_layout.addSpacing(10)

        # 复制按钮
        self.copy_btn = QPushButton('复制文本', self)
        self.copy_btn.setFixedHeight(30)
        self.copy_btn.clicked.connect(self.copy_text)
        self.copy_btn.setStyleSheet('''
            QPushButton {
                background-color: #E0E0E0;
                border: none;
                border-radius: 4px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #D0D0D0;
            }
        ''')
        button_layout.addWidget(self.copy_btn)
        
        # 添加弹性空间，使按钮靠左对齐
        button_layout.addStretch()
        
        # 将按钮布局添加到主布局
        layout.addLayout(button_layout)

        # 创建水平布局来放置预览和文本框
        h_layout = QHBoxLayout()
        h_layout.setSpacing(20)  # 设置水平布局的间距
        
        # 左侧预览区域
        preview_layout = QVBoxLayout()
        preview_layout.setSpacing(5)  # 减小预览区域的垂直间距
        
        preview_label = QLabel('截图预览')
        preview_label.setFixedHeight(20)  # 设置标签高度
        preview_label.setStyleSheet('font-size: 12px; color: #666;')  # 设置字体样式
        preview_layout.addWidget(preview_label)
        
        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(500, 400)  # 统一最小尺寸
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet('''
            QLabel {
                border: 1px solid #ccc;
                background-color: #f0f0f0;
                border-radius: 4px;
            }
        ''')
        preview_layout.addWidget(self.preview_label)
        h_layout.addLayout(preview_layout)

        # 右侧文本区域
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)  # 减小文本区域的垂直间距
        
        text_label = QLabel('识别结果')
        text_label.setFixedHeight(20)  # 设置标签高度
        text_label.setStyleSheet('font-size: 12px; color: #666;')  # 设置字体样式
        text_layout.addWidget(text_label)
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setMinimumSize(500, 400)  # 统一最小尺寸
        self.text_edit.setPlaceholderText('识别结果将显示在这里...')
        self.text_edit.setStyleSheet('''
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
        ''')
        text_layout.addWidget(self.text_edit)
        h_layout.addLayout(text_layout)

        # 设置左右两侧的宽度比例为1:1
        h_layout.setStretch(0, 1)  # 预览区域占1份
        h_layout.setStretch(1, 1)  # 文本区域占1份

        # 将水平布局添加到主布局
        layout.addLayout(h_layout)

        # 创建状态栏
        self.statusBar()

    def setup_hotkey(self):
        # 注册全局快捷键 Alt+C
        try:
            add_hotkey('alt+c', self.safe_start_capture)
        except Exception as e:
            print(f"注册快捷键失败: {str(e)}")

    def safe_start_capture(self):
        # 使用QTimer确保在主线程中执行
        if not self.is_capturing:
            QTimer.singleShot(0, self.start_capture)

    def setup_tray(self):
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(create_icon())
        
        # 创建托盘菜单
        tray_menu = QMenu()
        capture_action = QAction('开始截图 (Alt+C)', self)
        capture_action.triggered.connect(self.start_capture)
        
        copy_action = QAction('复制文本 (Ctrl+C)', self)
        copy_action.triggered.connect(self.copy_text)
        
        reset_action = QAction('重置窗口', self)
        reset_action.triggered.connect(self.reset_size)
        
        quit_action = QAction('退出', self)
        quit_action.triggered.connect(self.close_app)
        
        tray_menu.addAction(capture_action)
        tray_menu.addAction(copy_action)
        tray_menu.addAction(reset_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def close_app(self):
        # 移除快捷键
        try:
            remove_hotkey('alt+c')
        except Exception as e:
            print(f"注销快捷键失败: {str(e)}")
        # 关闭应用
        QApplication.quit()

    def closeEvent(self, event):
        # 保存窗口位置和大小
        self.settings.setValue('geometry', self.geometry())
        # 窗口关闭时触发
        self.close_app()
        event.accept()

    def start_capture(self):
        if self.is_capturing:
            return
        self.is_capturing = True
        
        # 先最小化窗口
        self.showMinimized()
        # 等待一下让动画完成
        QTimer.singleShot(200, self._do_capture)

    def _do_capture(self):
        # 完全隐藏窗口
        self.hide()
        # 等待一下让窗口完全隐藏
        QApplication.processEvents()
        self.screen = ScreenshotOverlay()
        self.screen.finished.connect(self.handle_screenshot_finished)
        self.screen.show()

    def handle_screenshot_finished(self, geometry):
        self.is_capturing = False
        if geometry.width() > 0 and geometry.height() > 0:
            # 如果有选择区域，则处理截图
            self.process_screenshot(geometry)
        else:
            # 如果没有选择区域（按ESC取消），则直接恢复窗口
            self.showNormal()

    def process_screenshot(self, geometry):
        # 先不显示主窗口，等处理完再显示
        if geometry.width() > 0 and geometry.height() > 0:
            # 确保坐标为正数
            x1, y1 = min(geometry.x(), geometry.x() + geometry.width()), min(geometry.y(), geometry.y() + geometry.height())
            x2, y2 = max(geometry.x(), geometry.x() + geometry.width()), max(geometry.y(), geometry.y() + geometry.height())
            
            try:
                # 获取截图
                screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                
                # 恢复并显示窗口
                self.showNormal()
                QApplication.processEvents()
                
                # 先显示预览图
                self.update_preview(screenshot)
                
                # 显示识别中的提示
                self.text_edit.setText('正在识别中...')
                QApplication.processEvents()  # 立即更新界面
                
                # 进行OCR识别
                result = self.ocr.process_image(np.array(screenshot))
                self.text_edit.setText(result)
            except Exception as e:
                self.text_edit.setText(f'截图失败: {str(e)}')
                self.showNormal()  # 确保出错时也能显示窗口

    def update_preview(self, screenshot):
        # 转换为QPixmap并显示预览
        if self.current_screenshot:
            self.current_screenshot = None  # 释放之前的截图
        
        # 调整图片大小以适应预览区域，保持原始比例
        preview_width = 500  # 统一预览区域宽度
        preview_height = 400  # 统一预览区域高度
        
        # 将PIL Image转换为QPixmap
        screenshot_array = np.array(screenshot)
        height, width = screenshot_array.shape[:2]
        
        # 计算缩放比例，保持宽高比
        scale = min(preview_width/width, preview_height/height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # 缩放图片
        screenshot_small = screenshot.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 创建RGB格式的QImage
        qimage = QImage(screenshot_small.convert('RGB').tobytes(), 
                       new_width, new_height, 
                       3 * new_width,  # 每行字节数 = 宽度 * 3（RGB）
                       QImage.Format.Format_RGB888)
        
        # 转换为QPixmap并显示
        self.current_screenshot = QPixmap.fromImage(qimage)
        
        # 创建背景pixmap
        background = QPixmap(preview_width, preview_height)
        background.fill(QColor('#f0f0f0'))
        
        # 在背景中央绘制截图
        painter = QPainter(background)
        x = (preview_width - new_width) // 2
        y = (preview_height - new_height) // 2
        painter.drawPixmap(x, y, self.current_screenshot)
        painter.end()
        
        # 显示最终结果
        self.preview_label.setPixmap(background)
        QApplication.processEvents()  # 立即更新界面

    def center(self):
        # 获取屏幕几何信息
        screen = QApplication.primaryScreen().geometry()
        # 获取窗口几何信息
        size = self.geometry()
        # 计算居中位置
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        # 移动窗口
        self.move(x, y)

    def restore_window_position(self):
        # 恢复窗口位置和大小
        if self.settings.contains('geometry'):
            geometry = self.settings.value('geometry')
            if isinstance(geometry, QRect):  # 确保获取到的是有效的几何信息
                # 确保窗口位置在当前屏幕范围内
                screen = QApplication.primaryScreen().geometry()
                if (geometry.x() < screen.width() and geometry.y() < screen.height() and
                    geometry.x() + geometry.width() > 0 and geometry.y() + geometry.height() > 0):
                    # 确保窗口大小不小于最小尺寸
                    width = max(geometry.width(), self.minimumWidth())
                    height = max(geometry.height(), self.minimumHeight())
                    # 设置位置和大小
                    self.setGeometry(geometry.x(), geometry.y(), width, height)
                else:
                    # 如果位置无效，使用默认大小并居中显示
                    self.resize(1200, 800)
                    self.center()
            else:
                # 如果几何信息无效，使用默认大小并居中显示
                self.resize(1200, 800)
                self.center()

    def reset_size(self):
        # 重置窗口大小和位置
        self.resize(1200, 800)
        self.center()
        self.settings.remove('geometry')  # 清除保存的位置信息

    def setup_shortcuts(self):
        """设置快捷键"""
        # 复制文本快捷键 (Ctrl+C)
        copy_shortcut = QShortcut(QKeySequence.StandardKey.Copy, self)
        copy_shortcut.activated.connect(self.copy_text)
        
        # 在按钮上显示快捷键提示
        self.copy_btn.setText('复制文本 (Ctrl+C)')
        self.copy_btn.setToolTip('使用 Ctrl+C 快捷键复制文本')

    def copy_text(self):
        """复制识别结果到剪贴板"""
        text = self.text_edit.toPlainText()
        if text and text != '识别结果将显示在这里...' and text != '正在识别中...':
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage('文本已复制到剪贴板', 2000)  # 显示2秒
        else:
            self.statusBar().showMessage('没有可复制的文本', 2000)  # 显示2秒 
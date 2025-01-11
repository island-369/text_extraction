import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import ScreenshotWindow

def main():
    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName('截图OCR工具')
    app.setApplicationVersion('1.0.0')
    
    # 创建并显示主窗口
    window = ScreenshotWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
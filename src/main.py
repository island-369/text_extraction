import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import ScreenshotWindow

def main():
    app = QApplication(sys.argv)
    window = ScreenshotWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
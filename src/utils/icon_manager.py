import os
from PyQt6.QtGui import QIcon, QPixmap, QColor

def create_icon():
    # 从文件创建图标
    icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'icon.png')
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    else:
        # 如果找不到图标文件，创建一个默认的纯色图标
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(0, 120, 212))  # 使用蓝色
        return QIcon(pixmap) 
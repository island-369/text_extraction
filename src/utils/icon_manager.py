from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor

def create_icon():
    """创建一个简单的应用图标"""
    # 创建一个32x32的图标
    icon_size = 32
    pixmap = QPixmap(icon_size, icon_size)
    pixmap.fill(QColor(0, 120, 212))  # 使用蓝色背景
    
    # 创建画笔
    painter = QPainter(pixmap)
    painter.setPen(QColor(255, 255, 255))  # 使用白色画笔
    
    # 绘制一个简单的相机图标
    margin = 6
    painter.drawRect(margin, margin, icon_size - 2*margin, icon_size - 2*margin)
    painter.drawEllipse(icon_size//2 - 4, icon_size//2 - 4, 8, 8)
    
    # 结束绘制
    painter.end()
    
    return QIcon(pixmap) 
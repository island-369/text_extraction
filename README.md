# Screenshot Text Extraction Tool | 屏幕截图，文字提取工具

A simple screenshot OCR tool with hotkey support and multi-language recognition.

一个简单易用的屏幕截图文字提取工具，支持快捷键操作和中英文识别。

## Preview | 运行效果

![Screenshot](docs/screenshot.png)

## Features | 功能特点

- Clean and intuitive interface | 简洁的图形界面
- Hotkey support (Alt+C) | 支持快捷键（Alt+C）快速截图
- Mouse selection for screenshot | 支持鼠标框选区域
- Real-time preview | 实时预览截图
- Multi-language recognition | 支持中英文识别
- System tray support | 系统托盘常驻
- Auto-save window position | 自动保存窗口位置

## Project Structure | 项目结构

```
text_extraction/
├── assets/                # Resources | 资源文件
│   └── icon.png          # Icon file | 图标文件
├── src/                  # Source code | 源代码
│   ├── ui/              # User Interface | 用户界面相关
│   │   ├── main_window.py     # Main window | 主窗口类
│   │   └── screenshot_overlay.py  # Screenshot layer | 截图覆盖层
│   ├── utils/           # Utilities | 工具函数
│   │   ├── icon_manager.py    # Icon management | 图标管理
│   │   └── hotkey_manager.py  # Hotkey management | 快捷键管理
│   ├── ocr/             # OCR related | OCR相关
│   │   └── paddle_ocr.py      # OCR processor | OCR处理器
│   └── main.py          # Program entry | 程序入口
├── requirements.txt     # Dependencies | 依赖文件
└── run.bat            # Run script | 运行脚本
```

## Requirements | 环境要求

- Windows 10/11
- Python 3.7+
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

## Installation | 安装步骤

1. Create virtual environment (recommended) | 创建虚拟环境（推荐）：
```bash
conda create -n pdf_totext python=3.8
conda activate pdf_totext
```

2. Install dependencies | 安装依赖：
```bash
pip install -r requirements.txt
```

3. Install Visual C++ Redistributable (if needed) | 安装 Visual C++ Redistributable（如果需要）：
Run `setup.bat` to automatically download and install required runtime | 运行 `setup.bat` 会自动下载并安装所需的运行库。

## Usage | 使用方法

1. Run the program | 运行程序：
   - Double click `run.bat` | 双击 `run.bat`
   - Or run in command line | 或在命令行中运行：`python src/main.py`

2. Screenshot operations | 截图操作：
   - Click "Start Screenshot" button or press `Alt+C` | 点击"开始截图"按钮或按 `Alt+C`
   - Hold left mouse button to select area | 按住左键拖动选择区域
   - Release to capture | 释放左键完成截图
   - Right click to cancel | 右键取消当前选择
   - Press ESC to exit | ESC键退出截图

3. Interface operations | 界面操作：
   - Left side shows preview | 左侧显示截图预览
   - Right side shows recognized text | 右侧显示识别文本
   - Window size is adjustable | 可以调整窗口大小
   - Click "Reset Window" to restore default size | 点击"重置窗口"恢复默认大小

4. System tray | 系统托盘：
   - Program can be minimized to system tray | 程序可以最小化到系统托盘
   - Right click tray icon for options | 右键托盘图标可以：
     - Start Screenshot | 开始截图
     - Reset Window | 重置窗口
     - Exit | 退出程序

## Development | 开发说明

- `src/ui/`: UI related code | 包含所有界面相关代码
- `src/utils/`: Utility functions and managers | 包含工具函数和管理类
- `src/ocr/`: OCR processing code | 包含OCR处理相关代码

## Notes | 注意事项

1. OCR model will be downloaded automatically on first run | 首次运行时会自动下载OCR模型文件
2. Make sure correct version of Visual C++ Redistributable is installed | 确保安装了正确版本的Visual C++ Redistributable
3. If hotkey conflicts, you can modify it in source code | 如果快捷键冲突，可以修改源码中的快捷键设置

## Feedback | 问题反馈

If you encounter any issues or have suggestions for improvement, please submit an Issue.
如果遇到问题或有改进建议，请提交Issue。 
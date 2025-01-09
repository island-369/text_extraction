# Screenshot OCR Tool | 截图OCR文字识别工具

A desktop application for extracting text from screen using PaddleOCR. Support both English and Chinese recognition.

一个简单的桌面应用程序，可以通过鼠标框选屏幕区域来识别其中的文字。支持中英文识别，使用PaddleOCR作为识别引擎。

## Features | 功能特点

- Simple and intuitive GUI interface | 简单的图形界面
- Mouse selection for screenshot area | 支持鼠标框选区域
- Support both English and Chinese text recognition | 支持中英文识别
- Real-time recognition results | 实时显示识别结果
- Shortcut support (ESC to cancel) | 支持快捷键（ESC取消截图）

## Requirements | 环境要求

- Windows 10/11
- Python 3.7+
- Required packages are listed in requirements.txt | 所需Python包已在requirements.txt中列出

## Installation | 安装步骤

1. Clone the repository | 克隆仓库：
```bash
git clone https://github.com/xqy853174787/text-extraction.git
cd text-extraction
```

2. Create and activate virtual environment | 创建并激活虚拟环境：
```bash
conda create -n pdf_totext python=3.10
conda activate pdf_totext
```

3. Install dependencies | 安装依赖：
```bash
pip install -r requirements.txt
```

## Usage | 使用方法

1. Run the program | 运行程序：
```bash
python main.py
```

2. Click "Start Screenshot" button
3. Use the mouse to drag and select the area to be recognized
4. Release the mouse to automatically perform text recognition
5. Recognition results will be displayed in the main window

## Quick Start | 快速启动

To make it easier to use, the project provides two batch scripts:

- `setup.bat`: Run when the project is first used to configure the environment
- `run.bat`: Daily use, start the program

## Project Structure | 项目结构

```
.
├── main.py              # 主程序
├── requirements.txt     # 依赖包列表
├── setup.bat           # 环境配置脚本
├── run.bat            # 运行脚本
└── README.md          # 项目说明
```

## Technology Stack | 技术栈

- PyQt6: GUI framework
- PaddleOCR: OCR engine
- Pillow: Image processing
- NumPy: Data processing

## License | 许可证

MIT License

## Contribution | 贡献

Welcome to submit Issues and Pull Requests. 
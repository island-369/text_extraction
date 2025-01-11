@echo off
chcp 65001 >nul
title OCR文字识别工具
cls

echo ============================================
echo             正在启动程序...
echo ============================================

call env.bat
if %errorlevel% equ 0 (
    python src/main.py
) else (
    echo ============================================
    echo             错误：环境激活失败
    echo ============================================
    echo 请确保已经运行过 setup.bat 进行环境配置
    timeout /t 5 >nul
) 
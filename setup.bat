@echo off
chcp 65001 >nul
title 环境配置
cls
echo ============================================
echo             环境配置开始
echo ============================================

REM 检查是否已安装Visual C++ Redistributable
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/3] 正在安装 Visual C++ Redistributable...
    curl -L -o vc_redist.x64.exe https://aka.ms/vs/17/release/vc_redist.x64.exe
    start /wait vc_redist.x64.exe /quiet /norestart
    del vc_redist.x64.exe
) else (
    echo [1/3] Visual C++ Redistributable 已安装
)

echo [2/3] 正在激活 conda 环境...
call env.bat
if %errorlevel% neq 0 (
    echo 环境激活失败，请检查conda环境是否正确安装
    timeout /t 1 >nul
    exit /b 1
)

echo [3/3] 正在安装 Python 依赖包...
pip install -r requirements.txt

echo ============================================
echo             环境配置完成！
echo ============================================
echo 您现在可以双击 run.bat 来启动程序
timeout /t 1 >nul 
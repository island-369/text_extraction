@echo off
chcp 65001 >nul
echo 正在激活虚拟环境...
call conda activate pdf_totext
if %errorlevel% neq 0 (
    echo 错误：虚拟环境激活失败
    exit /b 1
) else (
    echo 虚拟环境已激活：pdf_totext
)
exit /b 0

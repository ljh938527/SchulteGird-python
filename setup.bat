@echo off
REM setup.bat - Python 依赖自动安装脚本

echo 正在检查 Python 环境...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo 错误: 未检测到 Python，请先安装 Python 并添加到系统环境变量
    pause
    exit /b 1
)

echo.
echo 是否使用清华源加速安装？(默认: N)
set /p USE_MIRROR="[Y/N] > "

set "USE_MIRROR=!USE_MIRROR:y=Y!"
set "USE_MIRROR=!USE_MIRROR:n=N!"

REM 根据选择设置镜像参数
if "!USE_MIRROR!"=="Y" (
    set MIRROR_URL=-i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
    echo 已启用清华源加速
) else (
    set MIRROR_URL=
    echo 使用默认 PyPI 源
)

echo 升级 pip 到最新版本...
python -m pip install --upgrade pip %MIRROR_URL%

echo 正在安装项目依赖...
python -m pip install -r requirements.txt %MIRROR_URL%

if %ERRORLEVEL% eq 0 (
    echo 依赖安装成功！
) else (
    echo 依赖安装失败，请检查网络或依赖配置
)
pause
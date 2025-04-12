@echo off

REM setup.bat - Python 依赖自动安装脚本

set MIRROR_URL=-i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
echo 已启用清华源加速

echo 升级 pip 到最新版本...
python -m pip install --upgrade pip %MIRROR_URL%

echo 正在安装项目依赖...
python -m pip install --upgrade pip %MIRROR_URL%

if %ERRORLEVEL% eq 0 (
    echo 依赖安装成功！
) else (
    echo 依赖安装失败，请检查网络或依赖配置
)
pause
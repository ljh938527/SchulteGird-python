@echo off

REM setup.bat - Python �����Զ���װ�ű�

set MIRROR_URL=-i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
echo �������廪Դ����

echo ���� pip �����°汾...
python -m pip install --upgrade pip %MIRROR_URL%

echo ���ڰ�װ��Ŀ����...
python -m pip install --upgrade pip %MIRROR_URL%

if %ERRORLEVEL% eq 0 (
    echo ������װ�ɹ���
) else (
    echo ������װʧ�ܣ������������������
)
pause
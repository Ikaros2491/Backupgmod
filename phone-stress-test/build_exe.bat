@echo off
REM Build PhoneLineStressTest.exe on Windows (run from this folder).
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm PhoneLineStressTest.spec
echo.
echo Built: dist\PhoneLineStressTest.exe
pause

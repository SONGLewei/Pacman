@echo off
echo [1] create virtual env pac_env...
python -m venv pac_env

echo [2] activate virtual env...
call pac_env\Scripts\activate.bat

echo [3] install dependent...
pip install -r requirements.txt

echo [4] Start training!
python src\train.py

echo.
pause
@echo off
REM ============================================================
REM  MonsterDeleter 打包脚本（PyInstaller）
REM  运行前请先：  pip install -r requirements.txt
REM  产物： dist\MonsterDeleter.exe （单文件、无控制台窗口）
REM ============================================================
setlocal
cd /d "%~dp0"

echo [1/3] 检查 PyInstaller...
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo 未安装 PyInstaller，正在安装...
    pip install pyinstaller
)

echo [2/3] 生成怪兽动画与图标（若 assets 已存在会重新生成）...
python scripts\generate_monster.py
python scripts\make_icon.py

echo [3/3] 打包单文件 exe ...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name MonsterDeleter ^
    --icon assets\monster.ico ^
    --add-data "assets\monster.gif;assets" ^
    main.py

if errorlevel 1 (
    echo.
    echo 打包失败，请查看上方报错。
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  打包完成： dist\MonsterDeleter.exe
echo  下一步：编辑 install_menu.reg 中的 EXE_PATH 指向它，再双击导入
echo ============================================================
pause

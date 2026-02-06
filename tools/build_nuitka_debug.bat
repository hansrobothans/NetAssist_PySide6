@echo off
chcp 65001 >nul
echo ========================================
echo   调试助手工具 - Nuitka编译 (调试版)
echo   模式: Debug (保留控制台)
echo ========================================
echo.

REM 切换到项目根目录
cd /d "%~dp0.."
echo 工作目录: %cd%
echo.

REM 从 version.py 读取版本信息
for /f "tokens=2 delims==" %%a in ('findstr /c:"__version__ =" version.py') do set "VERSION=%%a"
for /f "tokens=2 delims==" %%a in ('findstr /c:"__app_name__ =" version.py') do set "APP_NAME=%%a"
REM 去除引号和空格
set VERSION=%VERSION:"=%
set VERSION=%VERSION: =%
set APP_NAME=%APP_NAME:"=%
set APP_NAME=%APP_NAME: =%

echo 应用名称: %APP_NAME%
echo 版本号: %VERSION%
echo.

REM 设置目录和文件名
set "BUILD_DIR=release\Nuitka_build_debug"
set "RELEASE_DIR=release\%APP_NAME%_V%VERSION%_debug"
set "EXE_NAME=%APP_NAME%_debug.exe"

echo 编译目录: %BUILD_DIR%
echo 输出目录: %RELEASE_DIR%
echo 可执行文件: %EXE_NAME%
echo.

REM 激活环境
echo [1/3] 激活环境...
call conda activate Py310
if errorlevel 1 (
    echo 环境激活失败
    pause
    exit /b 1
)
echo 环境已激活
echo.

REM 清理旧文件 (保留 main.build 加速编译)
echo [2/3] 清理旧文件...
if exist "%BUILD_DIR%\main.dist" rmdir /s /q "%BUILD_DIR%\main.dist"
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
echo 清理完成 (保留 main.build 加速下次编译)
echo.

REM 创建目录
if not exist "release" mkdir "release"
if not exist "%BUILD_DIR%" mkdir "%BUILD_DIR%"

REM 开始编译 (保留控制台以便调试)
echo [3/3] 开始编译 (调试模式)...
echo.

python -m nuitka ^
    --standalone ^
    --assume-yes-for-downloads ^
    --enable-plugin=pyside6 ^
    --nofollow-import-to=matplotlib ^
    --nofollow-import-to=scipy ^
    --nofollow-import-to=pandas ^
    --nofollow-import-to=tkinter ^
    --include-package=lib ^
    --include-package=models ^
    --include-package=services ^
    --include-package=viewmodels ^
    --include-package=views ^
    --include-data-dir=configs=configs ^
    --include-data-dir=resources/logo=resources/logo ^
    --windows-icon-from-ico=resources/logo/application.ico ^
    --output-dir="%BUILD_DIR%" ^
    --show-progress ^
    main.py

if errorlevel 1 (
    echo 编译失败
    pause
    exit /b 1
)

echo.
echo 编译完成！
echo.

REM 后处理
echo [后处理] 组织文件结构...

REM 复制 main.dist 到发布目录
xcopy "%BUILD_DIR%\main.dist" "%RELEASE_DIR%\" /E /I /Y >nul 2>&1
echo 文件已复制到发布目录

REM 重命名主程序
if exist "%RELEASE_DIR%\main.exe" (
    ren "%RELEASE_DIR%\main.exe" "%EXE_NAME%"
    echo 主程序已重命名
)

REM 复制配置文件
if not exist "%RELEASE_DIR%\configs" mkdir "%RELEASE_DIR%\configs"
copy "configs\*.json" "%RELEASE_DIR%\configs\" >nul 2>&1
echo 配置文件已复制
echo.

REM 显示结果
echo ========================================
echo   编译成功完成！
echo ========================================
echo.
echo 输出目录: %RELEASE_DIR%
echo 可执行文件: %RELEASE_DIR%\%EXE_NAME%
echo.
echo 运行测试:
echo   cd %RELEASE_DIR%
echo   %EXE_NAME%
echo.
pause

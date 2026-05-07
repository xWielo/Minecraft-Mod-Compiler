@echo off
:: Minecraft Mod Builder - Build .exe for Windows
:: Requires Python 3.8+ and PyInstaller

echo ========================================
echo   Minecraft Mod Builder - Build Script
echo ========================================
echo.

:: Check Python
python --version >NUL 2>&1
if errorlevel 1 (
    echo [BLAD] Python nie jest zainstalowany lub nie jest w PATH.
    echo Pobierz z: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Install/upgrade PyInstaller
echo [*] Instalowanie PyInstaller...
pip install pyinstaller --quiet --upgrade
if errorlevel 1 (
    echo [BLAD] Nie mozna zainstalowac PyInstaller.
    pause
    exit /b 1
)

:: Build .exe
echo [*] Budowanie pliku .exe...
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "MinecraftModBuilder" ^
    --clean ^
    main.py

if errorlevel 1 (
    echo.
    echo [BLAD] Budowanie nieudane!
    pause
    exit /b 1
)

echo.
echo ========================================
echo [OK] Sukces!
echo Plik EXE: dist\MinecraftModBuilder.exe
echo ========================================
pause

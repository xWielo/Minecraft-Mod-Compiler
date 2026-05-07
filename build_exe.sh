#!/bin/bash
# Minecraft Mod Builder - Build script for Linux/macOS

set -e

echo "========================================"
echo "  Minecraft Mod Builder - Build Script"
echo "========================================"
echo

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "[BLAD] Python3 nie jest zainstalowany."
    exit 1
fi

echo "[*] Instalowanie PyInstaller..."
pip3 install pyinstaller --quiet --upgrade

echo "[*] Budowanie aplikacji..."
echo

pyinstaller \
    --onefile \
    --windowed \
    --name "MinecraftModBuilder" \
    --clean \
    main.py

echo
echo "========================================"
echo "[OK] Sukces!"
echo "Plik: dist/MinecraftModBuilder"
echo "========================================"

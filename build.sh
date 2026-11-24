#!/usr/bin/env bash
# Builds build/central-command.exe with zig (Linux, macOS or Windows via Git Bash). Needs Python 3 + Pillow for the icons.
# Copy the devices folder beside central-command.exe when installing.
set -euo pipefail
cd "$(dirname "$0")"
ZIG="${ZIG:-zig}"
mkdir -p build
# Every device definition is checked against simulated hardware first (docs/devices.md).
"$ZIG" cc -O1 tools/devtest.c -o build/devtest
build/devtest devices/*.ini
# Two tray icons: white for a dark taskbar, dark for a light one.
python3 tools/make_icon.py build/central-command.ico
python3 tools/make_icon.py build/central-command-light.ico dark
cp src/central-command.rc build/
"$ZIG" cc -target x86_64-windows-gnu -Os -s -municode -Wl,--subsystem,windows \
  src/main.c build/central-command.rc -o build/central-command.exe \
  -lkernel32 -luser32 -lshell32 -ladvapi32 -lsetupapi -lhid -lpowrprof -lwtsapi32 -ldxva2 -ldwmapi -lgdi32
ls -l build/central-command.exe

@echo off
REM MochiPet Build & Deploy Script
REM This script automatically rebuilds the .exe and creates a ZIP distribution

echo.
echo ====================================
echo   MochiPet Build & Deploy Script
echo ====================================
echo.

REM Step 1: Rebuild the .exe with PyInstaller
echo [1/3] Rebuilding MochiPet.exe...
pyinstaller MochiPet.spec

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PyInstaller build failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Creating ZIP distribution...

REM Step 2: Create ZIP file (requires PowerShell or 7-Zip)
REM Using PowerShell to create ZIP
powershell -Command "Compress-Archive -Path 'dist\MochiPet.exe' -DestinationPath 'MochiPet.zip' -Force"

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: ZIP creation failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Recompiling installer...

REM Step 3: Compile the installer with InnoSetup (optional)
REM Try 64-bit installation first, then 32-bit
if exist "C:\Program Files\Inno Setup 7\ISCC.exe" (
    "C:\Program Files\Inno Setup 7\ISCC.exe" MochiPet-Installer.iss
) else if exist "C:\Program Files (x86)\Inno Setup 7\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 7\ISCC.exe" MochiPet-Installer.iss
) else (
    echo WARNING: Inno Setup 7 not found. Skipping installer build.
)

echo.
echo ====================================
echo   Build Complete!
echo ====================================
echo.
echo Updated files:
echo   - ZIP Distribution:  MochiPet.zip (recommended for users)
echo   - Direct EXE:        dist\MochiPet.exe
echo   - Installer:         installer\MochiPet-Setup.exe (optional)
echo.
echo To distribute: Share MochiPet.zip with users
echo Users: Extract ZIP and run MochiPet.exe
echo.
pause

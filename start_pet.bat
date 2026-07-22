@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

rem Start the pet without showing a console window.
if exist "%SCRIPT_DIR%.venv\Scripts\pythonw.exe" (
    start "Mochi Pet" "%SCRIPT_DIR%.venv\Scripts\pythonw.exe" "%SCRIPT_DIR%start_pet.pyw"
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        start "Mochi Pet" py "%SCRIPT_DIR%start_pet.pyw"
    ) else (
        start "Mochi Pet" python "%SCRIPT_DIR%start_pet.pyw"
    )
)
exit /b

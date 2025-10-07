@echo off
REM ============================================================================
REM SubFast - Context Menu Installer
REM Standalone installer - no PowerShell needed
REM ============================================================================

REM Check for Administrator privileges and auto-elevate if needed
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ==========================================
    echo   Administrator Privileges Required
    echo ==========================================
    echo.
    echo SubFast needs Administrator privileges to
    echo add context menu registry entries.
    echo.
    echo A new window will open - please click 'Yes'
    echo on the UAC prompt.
    echo.
    echo Press any key to continue...
    pause >nul
    powershell -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit
)

REM Clear screen and show branding
cls
echo ==========================================
echo    ____        _     _____          _   
echo   / ___^| _   _^| ^|__ ^|  ___^|_ _  ___^| ^|_ 
echo   \___ \^| ^| ^| ^| '_ \^| ^|_ / _` ^|/ __^| ^|__^|
echo    ___) ^| ^|_^| ^| ^|_) ^|  _^| (_^| ^\__ \ ^|_ 
echo   ^|____/ \__,_^|_.__/^|_^|  \__,_^|___/\__^|
echo.
echo    Fast subtitle renaming and embedding
echo.
echo ==========================================
echo          Context Menu Installer
echo ==========================================
echo.

REM Get installation path (where this script is located)
set "INSTALL_PATH=%~dp0"
set "INSTALL_PATH=%INSTALL_PATH:~0,-1%"

REM Convert to registry format (escape backslashes)
set "REG_PATH=%INSTALL_PATH:\=\\%"
set "ICON_PATH=%REG_PATH%\\resources\\subfast_logo.ico"
set "RENAME_SCRIPT=%REG_PATH%\\scripts\\subfast_rename.py"
set "EMBED_SCRIPT=%REG_PATH%\\scripts\\subfast_embed.py"

echo [INFO] Installation path: %INSTALL_PATH%
echo.

REM Validate required files
if not exist "%INSTALL_PATH%\scripts\subfast_rename.py" (
    echo [ERROR] Missing required file: scripts\subfast_rename.py
    goto ERROR
)
if not exist "%INSTALL_PATH%\scripts\subfast_embed.py" (
    echo [ERROR] Missing required file: scripts\subfast_embed.py
    goto ERROR
)
if not exist "%INSTALL_PATH%\resources\subfast_logo.ico" (
    echo [ERROR] Missing required file: resources\subfast_logo.ico
    goto ERROR
)

echo [OK] All required files found
echo.
echo [INFO] Registering context menu entries...
echo.

REM Create registry entries
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" /f /ve /t REG_SZ /d "" >nul 2>&1
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" /f /v "MUIVerb" /t REG_SZ /d "SubFast" >nul 2>&1
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" /f /v "SubCommands" /t REG_SZ /d "" >nul 2>&1
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" /f /v "Icon" /t REG_SZ /d "%ICON_PATH%" >nul 2>&1

reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell" /f >nul 2>&1

reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\01-Rename" /f /v "MUIVerb" /t REG_SZ /d "Rename subtitles" >nul 2>&1
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\01-Rename\command" /f /ve /t REG_SZ /d "\"C:\\Windows\\py.exe\" \"%RENAME_SCRIPT%\" \"%%V\"" >nul 2>&1

reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\02-Embed" /f /v "MUIVerb" /t REG_SZ /d "Embed subtitles" >nul 2>&1
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\02-Embed\command" /f /ve /t REG_SZ /d "\"C:\\Windows\\py.exe\" \"%EMBED_SCRIPT%\" \"%%V\"" >nul 2>&1

if %errorLevel% neq 0 goto ERROR

echo ==========================================
echo   SUCCESS! Context menu installed
echo ==========================================
echo.
echo Location: %INSTALL_PATH%
echo.
echo Closing in 10 seconds... (press any key to exit now)
timeout /t 10
exit /b 0

:ERROR
echo.
echo [ERROR] Failed to install context menu!
echo.
echo Make sure:
echo   - You clicked 'Yes' on the UAC prompt
echo   - All required files are present
echo.
pause
exit /b 1

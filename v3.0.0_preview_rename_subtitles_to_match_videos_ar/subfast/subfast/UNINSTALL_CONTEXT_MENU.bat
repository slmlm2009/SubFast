@echo off
REM ============================================================================
REM SubFast - Context Menu Uninstaller
REM Standalone uninstaller - no PowerShell needed
REM ============================================================================

REM Check for Administrator privileges and auto-elevate if needed
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
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
echo         Context Menu Uninstaller
echo ==========================================
echo.

echo [INFO] Removing SubFast context menu entries...
echo.

REM Check if registry key exists
reg query "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] SubFast context menu is not installed
    echo.
) else (
    REM Remove registry entries
    reg delete "HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" /f >nul 2>&1
    if %errorLevel% neq 0 goto ERROR
    
    echo ==========================================
    echo   SUCCESS! Context menu removed
    echo ==========================================
    echo.
)

echo Closing in 10 seconds... (press any key to exit now)
timeout /t 10
exit /b 0

:ERROR
echo.
echo [ERROR] Failed to remove context menu!
echo.
echo Make sure you clicked 'Yes' on the UAC prompt.
echo.
pause
exit /b 1

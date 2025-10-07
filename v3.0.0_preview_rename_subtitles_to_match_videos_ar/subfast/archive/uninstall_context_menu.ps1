# ============================================================================
# SubFast - Context Menu Uninstaller
# Removes SubFast context menu entries
# ============================================================================

# Self-elevate if not running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Requesting Administrator privileges..." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   ____        _     _____          _   " -ForegroundColor Cyan
Write-Host "  / ___| _   _| |__ |  ___|_ _  ___| |_ " -ForegroundColor Cyan
Write-Host "  \___ \| | | | '_ \| |_ / _` |/ __| __|" -ForegroundColor Cyan
Write-Host "   ___) | |_| | |_) |  _| (_| |\__ \ |_ " -ForegroundColor Cyan
Write-Host "  |____/ \__,_|_.__/|_|  \__,_||___/\__|" -ForegroundColor Cyan
Write-Host "                                        " -ForegroundColor Cyan
Write-Host "   Fast subtitle renaming and embedding" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "        Context Menu Uninstaller" -ForegroundColor White
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[INFO] Removing SubFast context menu entries..." -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: This uninstaller only removes registry entries." -ForegroundColor Yellow
Write-Host "      It works regardless of where SubFast files are located." -ForegroundColor Yellow
Write-Host "      SubFast files are not deleted - only the context menu is removed." -ForegroundColor Yellow
Write-Host ""

try {
    # Check if registry key exists
    if (Test-Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast") {
        # Remove the entire SubFast menu tree
        Remove-Item -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" -Recurse -Force
        
        Write-Host ""
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host "  SUCCESS! Context menu removed" -ForegroundColor Green
        Write-Host "==========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "The SubFast context menu has been removed from Windows Explorer." -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "[INFO] SubFast context menu is not installed" -ForegroundColor Yellow
        Write-Host ""
    }
    
    Write-Host "Press any key to exit (auto-closes in 5 seconds)..." -ForegroundColor Yellow
    
    # Wait for key press or 5 seconds timeout
    $timeout = 5
    $startTime = Get-Date
    while ((Get-Date) -lt $startTime.AddSeconds($timeout)) {
        if ([Console]::KeyAvailable) {
            [Console]::ReadKey($true) | Out-Null
            break
        }
        Start-Sleep -Milliseconds 100
    }
    
} catch {
    Write-Host ""
    Write-Host "[ERROR] Failed to remove context menu:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure you run this script as Administrator!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit (auto-closes in 10 seconds)..." -ForegroundColor Yellow
    
    # Wait for key press or 10 seconds timeout on error
    $timeout = 10
    $startTime = Get-Date
    while ((Get-Date) -lt $startTime.AddSeconds($timeout)) {
        if ([Console]::KeyAvailable) {
            [Console]::ReadKey($true) | Out-Null
            break
        }
        Start-Sleep -Milliseconds 100
    }
    exit 1
}

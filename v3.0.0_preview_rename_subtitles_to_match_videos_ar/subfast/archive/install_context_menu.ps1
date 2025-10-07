# ============================================================================
# SubFast - Smart Context Menu Installer
# Auto-detects installation path and registers context menu
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
Write-Host "         Context Menu Installer" -ForegroundColor White
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get the directory where this script is located
$InstallPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "[INFO] Installation path detected: $InstallPath" -ForegroundColor Green

# Validate required files exist
$RequiredFiles = @(
    "$InstallPath\scripts\subfast_rename.py",
    "$InstallPath\scripts\subfast_embed.py",
    "$InstallPath\resources\subfast_logo.ico"
)

$MissingFiles = @()
foreach ($File in $RequiredFiles) {
    if (-not (Test-Path $File)) {
        $MissingFiles += $File
    }
}

if ($MissingFiles.Count -gt 0) {
    Write-Host "[ERROR] Missing required files:" -ForegroundColor Red
    foreach ($File in $MissingFiles) {
        Write-Host "  - $File" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Please ensure SubFast is properly installed." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] All required files found" -ForegroundColor Green
Write-Host ""

# Convert paths to registry format (double backslashes)
$RegPath = $InstallPath.Replace('\', '\\')
$IconPath = "$RegPath\\resources\\subfast_logo.ico"
$RenameScript = "$RegPath\\scripts\\subfast_rename.py"
$EmbedScript = "$RegPath\\scripts\\subfast_embed.py"

Write-Host "[INFO] Registering context menu entries..." -ForegroundColor Cyan

# Create registry entries
try {
    # Parent menu
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" -Name "MUIVerb" -Value "SubFast"
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" -Name "SubCommands" -Value ""
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast" -Name "Icon" -Value $IconPath
    
    # Create shell container
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell" -Force | Out-Null
    
    # Rename subtitles menu item
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\01-Rename" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\01-Rename" -Name "MUIVerb" -Value "Rename subtitles"
    
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\01-Rename\command" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\01-Rename\command" -Name "(Default)" -Value "`"C:\Windows\py.exe`" `"$RenameScript`" `"%V`""
    
    # Embed subtitles menu item
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\02-Embed" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\02-Embed" -Name "MUIVerb" -Value "Embed subtitles"
    
    New-Item -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\02-Embed\command" -Force | Out-Null
    Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\Directory\Background\shell\SubFast\shell\02-Embed\command" -Name "(Default)" -Value "`"C:\Windows\py.exe`" `"$EmbedScript`" `"%V`""
    
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "  SUCCESS! Context menu installed" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installation Details:" -ForegroundColor Cyan
    Write-Host "  Location: $InstallPath" -ForegroundColor White
    Write-Host "  Icon: $IconPath" -ForegroundColor White
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Cyan
    Write-Host "  1. Right-click on any folder background" -ForegroundColor White
    Write-Host "  2. Select 'SubFast' from context menu" -ForegroundColor White
    Write-Host "  3. Choose 'Rename subtitles' or 'Embed subtitles'" -ForegroundColor White
    Write-Host ""
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
    Write-Host "[ERROR] Failed to register context menu:" -ForegroundColor Red
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

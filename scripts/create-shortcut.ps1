# Create desktop shortcut for RDP connection script
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = "C:\Users\Rohit\Desktop"
$ShortcutPath = Join-Path $DesktopPath "Connect RDP.lnk"

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"C:\Users\Rohit\workspace\Personal\software\network-tools\scripts\connect-rdp.ps1`""
$Shortcut.WorkingDirectory = "C:\Users\Rohit\workspace\Personal\software\network-tools\scripts"
$Shortcut.IconLocation = "mstsc.exe,0"
$Shortcut.Description = "Connect to 192.168.68.74 via RDP"
$Shortcut.Save()

Write-Host "Shortcut created at: $ShortcutPath" -ForegroundColor Green
Write-Host "Right-click the shortcut and select 'Pin to taskbar'" -ForegroundColor Cyan

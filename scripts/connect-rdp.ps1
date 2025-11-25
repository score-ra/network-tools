# Connect to remote PC via RDP (single display)
# Target: 192.168.68.74
# User: MicrosoftAccount\ra-local

param(
    [string]$Computer = "192.168.68.74",
    [string]$Username = "MicrosoftAccount\ra-local"
)

# Build mstsc arguments for single display
# /v: target computer
# /span:0 or omit /multimon to use single display
$mstscArgs = "/v:$Computer"

Write-Host "Connecting to $Computer as $Username (single display)..." -ForegroundColor Cyan

# Launch Remote Desktop Connection
Start-Process mstsc -ArgumentList $mstscArgs

Write-Host "RDP connection initiated." -ForegroundColor Green

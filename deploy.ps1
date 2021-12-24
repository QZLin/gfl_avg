# Recommend Powershell-7
Set-Location $PSScriptRoot
$renpy_prj = Get-Content "tool/config.py" | Select-String -Pattern "RENPY_PROJECT\s*=\s*r?'(.*)'" | ForEach-Object { $_.Matches.Groups[1].value }
$renpy_prj = $renpy_prj -replace "\\\\", "\"
Write-Output "Renpy Project: $renpy_prj"
$target = "$renpy_prj\game"

&"./clean.ps1" "$target\script_level"

Copy-Item ./rpy/*.* $target/script_level -Force
Write-Output "Copy rpy/*.* to $target\script_level, copy rpy/script.rpy to $target"
Move-Item $target/script_level/script.rpy $target -Force

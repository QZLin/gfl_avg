#Requires -Version 7.0
function config($name) {
    return python -c "import tool.config;print(tool.config.$name)"
}

Push-Location $PSScriptRoot
#$renpy_prj = Get-Content "tool/config.py" | Select-String -Pattern "RENPY_PROJECT\s*=\s*r?'(.*)'" | ForEach-Object { $_.Matches.Groups[1].value }
#$renpy_prj = $renpy_prj -replace "\\\\", "\"
$renpy_prj = config("RENPY_PROJECT")
Write-Output "Renpy Project: $renpy_prj"
$target = [IO.Path]::Combine($renpy_prj, "game")
$scripts = [IO.Path]::Combine($target, "script_level")

&"./clean.ps1" $scripts

Copy-Item ./rpy/*.* $scripts -Force
Write-Output "Copy rpy/*.* to $scripts, copy rpy/script.rpy to $target"
Move-Item ([IO.Path]::Combine($scripts, "script.rpy")) $target -Force
Pop-Location

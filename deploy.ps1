#Requires -Version 7.0
function read_config($name)
{
    return python -c "import tool.config;print(tool.config.$name)"
}
function configs()
{
    return python -c `
    "from tool.config import *;import json;print(json.dumps(globals(),default=lambda _:''))" |
            ConvertFrom-Json
}
$cfg = configs("")

Push-Location $PSScriptRoot
$renpy_prj = $cfg.("RENPY_PROJECT")
Write-Output "Renpy Project: $renpy_prj"
$target = [IO.Path]::Combine($renpy_prj, "game")
$scripts = [IO.Path]::Combine($target, "script_level")

&"./clean.ps1" $scripts

Copy-Item ./rpy/*.* $scripts -Force
Write-Output "Copy rpy/*.* to $scripts, copy rpy/script.rpy to $target"
Move-Item ([IO.Path]::Combine($scripts, "script.rpy")) $target -Force
Pop-Location

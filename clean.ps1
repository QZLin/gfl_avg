param(
    [string]$target_path = "."
)

$current_path = Get-Location

Set-Location $target_path
Write-Output "Clean '*.rpyc','*.rpyc.bak' for $target_path"
Remove-Item ./*.rpyc
Remove-Item ./*.rpyc.bak

Set-Location $current_path
param(
    [string]$target_path = "."
)

Push-Location $target_path
Write-Output "Clean '*.rpyc','*.rpyc.bak' for $target_path"
Remove-Item ./*.rpyc
Remove-Item ./*.rpyc.bak

Pop-Location
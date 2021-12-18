param(
    [string]$target_path = "."
)

$current_path = Get-Location

cd $target_path
Write-Output "Clean '*.rpyc','*.rpyc.bak' for $target_path"
rm ./*.rpyc
rm ./*.rpyc.bak

cd $current_path
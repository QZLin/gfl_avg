param(
    [string]$target_path = "."
)

Push-Location $target_path
if (-not(Test-Path $target_path/".delete_confirm"))
{
    Write-Output "Not Confirmed Clean Dir $target_path Continue?"
    $r = New-Item $target_path/".delete_confirm" -Confirm
    if (-not $r)
    {
        $exit = $true
    }
}
if (-not $exit)
{
    Write-Output "Clean '*.rpyc','*.rpyc.bak' for $target_path"
    Remove-Item ./*.rpyc
    Remove-Item ./*.rpyc.bak
}

Pop-Location
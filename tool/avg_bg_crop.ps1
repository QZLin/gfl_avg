Push-Location ((Get-Item $PSScriptRoot).parent)
. venv/Scripts/Activate.ps1

function config($name) {
    return python -c "import tool.config;print(tool.config.$name)"
}

$image_path = config("AVG_BG_SOURCE")
$target_path = config("AVG_BG_TARGET")
Write-Output "SourceDir: $image_path,`nTargetDir$target_path"
# Pop-Location
# Push-Location $image_path
$sw = [Diagnostics.Stopwatch]::StartNew()
Get-ChildItem $image_path -Filter "*.png" | ForEach-Object {
    # Start-Process python -Args "tool/avg_bg_handle.pya", $_.FullName -RedirectStandardOutput (Join-Path $target_path $_.Name) -RedirectStandardError $true -Verbose
    # [io.file]::WriteAllBytes((Join-Path $target_path $_.Name),
    # (./tool/Invoke-BinaryProcess.ps1 python.exe -Output -ArgumentList "tool/avg_bg_handle.py", $_.FullName))
    Write-Output $_.Name
    $st = $sw.ElapsedMilliseconds
    python "tool/avg_bg_handle.py" $_.FullName -f (Join-Path $target_path $_.Name)
    Write-Output "$(($sw.ElapsedMilliseconds-$st)/1000)s"
}
$sw.Stop()
Write-Output "Finished,total:$($sw.ElapsedMilliseconds/1000)s"

Pop-Location
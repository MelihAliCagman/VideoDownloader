# Masaüstüne "YouTube İndirici" kısayolu oluşturur.
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$desktop = [Environment]::GetFolderPath("Desktop")
$sc = (New-Object -ComObject WScript.Shell).CreateShortcut("$desktop\YouTube Indirici.lnk")
$sc.TargetPath = "$root\.venv\Scripts\pythonw.exe"
$sc.Arguments = "main.py"
$sc.WorkingDirectory = $root
$sc.IconLocation = "$root\assets\icon.ico"
$sc.Description = "YouTube İndirici"
$sc.Save()
Write-Output "Kısayol oluşturuldu: $desktop\YouTube Indirici.lnk"


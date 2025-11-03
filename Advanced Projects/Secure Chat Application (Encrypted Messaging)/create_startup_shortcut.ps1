$batPath = 'C:\Users\vgree\OneDrive\Desktop\Cyber Security\VS Code\Cyber-Shield\Advanced Projects\Secure Chat Application (Encrypted Messaging)\run_server_user.bat'
$startup = [Environment]::GetFolderPath('Startup')
$lnkPath = Join-Path $startup 'SecureChatServerUser.lnk'

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($lnkPath)
$shortcut.TargetPath = $batPath
$shortcut.WorkingDirectory = Split-Path $batPath -Parent
$shortcut.WindowStyle = 1
$shortcut.Save()
Write-Output "Shortcut created at: $lnkPath"

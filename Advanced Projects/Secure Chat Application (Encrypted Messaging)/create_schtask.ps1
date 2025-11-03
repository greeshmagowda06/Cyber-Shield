# Create scheduled task for SecureChatServerUser (user-level)
$taskName = 'SecureChatServerUser'
$batPath = 'C:\Users\vgree\OneDrive\Desktop\Cyber Security\VS Code\Cyber-Shield\Advanced Projects\Secure Chat Application (Encrypted Messaging)\run_server_user.bat'
$logPath = 'C:\Users\vgree\OneDrive\Desktop\Cyber Security\VS Code\Cyber-Shield\Advanced Projects\Secure Chat Application (Encrypted Messaging)\server_user.log'

Try {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
} Catch {
}

$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument "/c `"$batPath`""
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -TaskName $taskName -Trigger $trigger -Action $action -Force
Start-ScheduledTask -TaskName $taskName
Start-Sleep -Seconds 2

Get-ScheduledTask -TaskName $taskName | Get-ScheduledTaskInfo | Format-List

if (Test-Path $logPath) {
    Get-Content -Path $logPath -Tail 50
} else {
    Write-Output 'LOG_NOT_FOUND'
}

netstat -ano | Select-String ':5000'

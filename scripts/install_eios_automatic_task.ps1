$ErrorActionPreference = 'Stop'

$taskName = 'EIOS Automatic Company Intelligence'
$runner = 'C:\Users\RBI\Desktop\EIOS\scripts\run_eios_automatic_cycle.ps1'

if (-not (Test-Path -LiteralPath $runner -PathType Leaf)) {
    throw "EIOS automatic-cycle runner is missing: $runner"
}

$arguments = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -File `"$runner`""
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $arguments
$trigger = New-ScheduledTaskTrigger -Daily -At '06:00'
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 2)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description 'Runs the governed EIOS company-intelligence collection cycle.' -Force | Out-Null

$task = Get-ScheduledTask -TaskName $taskName
$info = Get-ScheduledTaskInfo -TaskName $taskName
[pscustomobject]@{
    TaskName = $task.TaskName
    State = $task.State
    NextRunTime = $info.NextRunTime
    StartWhenAvailable = $task.Settings.StartWhenAvailable
    MultipleInstances = $task.Settings.MultipleInstances
    RunsOnBattery = -not $task.Settings.DisallowStartIfOnBatteries
}

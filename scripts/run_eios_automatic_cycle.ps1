$ErrorActionPreference = 'Stop'

$workspace = 'C:\Users\RBI\Desktop\EIOS'
$logDirectory = Join-Path $workspace 'data\runtime'
$logPath = Join-Path $logDirectory 'automatic_company_cycle.log'

New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
Set-Location -LiteralPath $workspace

& 'C:\Program Files\Python314\python.exe' -m scripts.run_automatic_company_cycle *>> $logPath
exit $LASTEXITCODE

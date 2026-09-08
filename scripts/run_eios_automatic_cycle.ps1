$ErrorActionPreference = 'Stop'

$workspace = 'C:\Users\RBI\Desktop\EIOS'
$logDirectory = Join-Path $workspace 'data\runtime'
$logPath = Join-Path $logDirectory 'automatic_company_cycle.log'

New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
Set-Location -LiteralPath $workspace

# Scheduled tasks do not inherit temporary terminal credentials. Keep local
# document retries and read-model refreshes running without attempting an
# unconfigured paid search. A user- or machine-level key activates live search.
if ([string]::IsNullOrWhiteSpace($env:TAVILY_API_KEY) -or $env:EIOS_LIVE_SEARCH_ENABLED -ne 'true') {
    $env:EIOS_OFFLINE_MODE = 'true'
    Add-Content -LiteralPath $logPath -Value "$(Get-Date -Format o) LIVE_SEARCH_DISABLED_OR_UNAVAILABLE: running governed offline cycle"
} else {
    $env:EIOS_OFFLINE_MODE = 'false'
}

& 'C:\Program Files\Python314\python.exe' -m scripts.run_automatic_company_cycle *>> $logPath
exit $LASTEXITCODE

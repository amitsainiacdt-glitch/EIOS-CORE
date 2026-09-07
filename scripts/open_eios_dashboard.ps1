param([switch]$CheckOnly, [switch]$NoBrowser, [switch]$Rebuild)

$ErrorActionPreference = 'Stop'

$dashboardBaseUrl = 'http://localhost:3000/'
# The desktop shortcut already targets this script. Open the current working
# graph section, with a fresh navigation key rather than an old home tab.
$dashboardUrl = 'http://localhost:3000/companies/coromandel?charts=3&desktopRefresh=' + [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() + '#financial-trends'
$workspaceDirectory = Split-Path -Parent $PSScriptRoot
$dashboardDirectory = Join-Path $workspaceDirectory 'local_status_dashboard'
$logDirectory = Join-Path $workspaceDirectory 'data\runtime\desktop'

function Test-EiosPort {
    & curl.exe --noproxy '*' --silent --fail --head --max-time 2 $dashboardBaseUrl *> $null
    return $LASTEXITCODE -eq 0
}

function Test-EiosReviewService {
    & curl.exe --noproxy '*' --silent --fail --max-time 2 'http://127.0.0.1:3001/health' *> $null
    return $LASTEXITCODE -eq 0
}

$dashboardIsRunning = Test-EiosPort

if ($CheckOnly) {
    [pscustomobject]@{ DashboardRunning = $dashboardIsRunning; ReviewServiceRunning = (Test-EiosReviewService); Opens = $dashboardUrl; Workspace = $workspaceDirectory }
    exit 0
}

New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
$launchKey = [guid]::NewGuid().ToString('N')
$reviewServiceRunning = Test-EiosReviewService
if (-not $reviewServiceRunning) {
    try {
        $pythonPath = (Get-Command python.exe -ErrorAction Stop).Source
        Start-Process -FilePath $pythonPath -ArgumentList 'scripts/local_company_fact_review_api.py' -WorkingDirectory $workspaceDirectory -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logDirectory "$launchKey-review.log") -RedirectStandardError (Join-Path $logDirectory "$launchKey-review-error.log")
    } catch {
        # A review-service failure must not prevent access to saved research.
        Write-Warning "EIOS review service could not start: $_"
    }
}

if (-not $dashboardIsRunning) {
    $hasBuild = Test-Path (Join-Path $dashboardDirectory 'dist\server\index.js')
    $startupCommand = if ($Rebuild -or -not $hasBuild) { '"npm run sync && npm run build && npm run start"' } else { '"npm run start"' }
    $dashboardProcess = Start-Process -FilePath 'C:\Windows\System32\cmd.exe' -ArgumentList '/d', '/s', '/c', $startupCommand -WorkingDirectory $dashboardDirectory -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $logDirectory "$launchKey-dashboard.log") -RedirectStandardError (Join-Path $logDirectory "$launchKey-dashboard-error.log")

    for ($attempt = 0; $attempt -lt 120; $attempt++) {
        Start-Sleep -Milliseconds 500
        if (Test-EiosPort) {
            break
        }
        if ($dashboardProcess.HasExited) { break }
    }
}

if (Test-EiosPort) {
    if (-not $NoBrowser) { Start-Process $dashboardUrl }
    exit 0
}

if ($NoBrowser) {
    Write-Error "EIOS could not start. See startup logs in $logDirectory"
    exit 1
}
Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show(
    "EIOS could not start. Diagnostic logs are saved in $logDirectory. Please share the latest dashboard-error log for help.",
    'EIOS Dashboard',
    'OK',
    'Warning'
) | Out-Null
exit 1

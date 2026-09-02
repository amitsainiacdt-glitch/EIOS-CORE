param([switch]$CheckOnly)

$ErrorActionPreference = 'Stop'

$dashboardBaseUrl = 'http://localhost:3000/'
# The desktop shortcut already targets this script. Open the current working
# graph section, with a fresh navigation key rather than an old home tab.
$dashboardUrl = 'http://localhost:3000/companies/coromandel?charts=3&desktopRefresh=' + [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() + '#financial-trends'
$dashboardDirectory = 'C:\Users\RBI\Desktop\EIOS\local_status_dashboard'
$workspaceDirectory = 'C:\Users\RBI\Desktop\EIOS'

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
    [pscustomobject]@{ DashboardRunning = $dashboardIsRunning; Opens = $dashboardUrl; Workspace = $workspaceDirectory }
    exit 0
}

$reviewServiceRunning = Test-EiosReviewService
if (-not $reviewServiceRunning) {
    Start-Process -FilePath 'C:\Program Files\Python314\python.exe' -ArgumentList 'scripts/local_company_fact_review_api.py' -WorkingDirectory $workspaceDirectory -WindowStyle Hidden
}

if (-not $dashboardIsRunning) {
    Start-Process -FilePath 'C:\Windows\System32\cmd.exe' -ArgumentList '/d', '/s', '/c', '"npm run sync && npm run build && npm run start"' -WorkingDirectory $dashboardDirectory -WindowStyle Hidden

    for ($attempt = 0; $attempt -lt 60; $attempt++) {
        Start-Sleep -Milliseconds 500
        if (Test-EiosPort) {
            break
        }
    }
}

if (Test-EiosPort) {
    Start-Process $dashboardUrl
    exit 0
}

Add-Type -AssemblyName PresentationFramework
[System.Windows.MessageBox]::Show(
    'EIOS could not start. Please wait a few seconds and double-click the EIOS Dashboard icon again.',
    'EIOS Dashboard',
    'OK',
    'Warning'
) | Out-Null
exit 1

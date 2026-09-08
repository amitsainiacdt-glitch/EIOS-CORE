$ErrorActionPreference = 'Stop'

$workspace = 'C:\Users\RBI\Desktop\EIOS'
$logDirectory = Join-Path $workspace 'data\runtime'
$logPath = Join-Path $logDirectory 'automatic_company_cycle.log'

New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
Set-Location -LiteralPath $workspace

# Scheduled tasks do not inherit temporary terminal credentials. Keep local
# document retries and read-model refreshes running without attempting an
# unconfigured paid search. The credential is protected by Windows DPAPI and
# decryptable only by the same Windows user that configured it.
$credentialPath = Join-Path $workspace 'data\runtime\credentials\tavily.dpapi'
$enabledPath = Join-Path $workspace 'data\runtime\credentials\live_search.enabled'
$liveSearchReady = (Test-Path -LiteralPath $credentialPath -PathType Leaf) -and (Test-Path -LiteralPath $enabledPath -PathType Leaf)
if ($liveSearchReady) {
    try {
        $secureKey = (Get-Content -LiteralPath $credentialPath -Raw).Trim() | ConvertTo-SecureString
        $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
        try { $env:TAVILY_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer) }
        finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
        $liveSearchReady = -not [string]::IsNullOrWhiteSpace($env:TAVILY_API_KEY)
    } catch {
        $liveSearchReady = $false
    }
}
if (-not $liveSearchReady) {
    $env:EIOS_OFFLINE_MODE = 'true'
    Add-Content -LiteralPath $logPath -Value "$(Get-Date -Format o) LIVE_SEARCH_DISABLED_OR_UNAVAILABLE: running governed offline cycle"
} else {
    $env:EIOS_OFFLINE_MODE = 'false'
}

& 'C:\Program Files\Python314\python.exe' -m scripts.run_automatic_company_cycle *>> $logPath
exit $LASTEXITCODE

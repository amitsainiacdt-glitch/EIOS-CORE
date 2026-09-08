$ErrorActionPreference = 'Stop'

$workspace = 'C:\Users\RBI\Desktop\EIOS'
$credentialPath = Join-Path $workspace 'data\runtime\credentials\tavily.dpapi'
if (-not (Test-Path -LiteralPath $credentialPath -PathType Leaf)) {
    throw 'EIOS live-search credential is not securely configured.'
}

$secureKey = (Get-Content -LiteralPath $credentialPath -Raw).Trim() | ConvertTo-SecureString
$pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
try { $env:TAVILY_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer) }
finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
$env:EIOS_OFFLINE_MODE = 'false'
Set-Location -LiteralPath $workspace
& 'C:\Program Files\Python314\python.exe' -m scripts.run_primary_indicator_canary @args
exit $LASTEXITCODE

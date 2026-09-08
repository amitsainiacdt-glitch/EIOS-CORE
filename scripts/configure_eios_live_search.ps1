$ErrorActionPreference = 'Stop'

$workspace = 'C:\Users\RBI\Desktop\EIOS'
$credentialDirectory = Join-Path $workspace 'data\runtime\credentials'
$credentialPath = Join-Path $credentialDirectory 'tavily.dpapi'
$enabledPath = Join-Path $credentialDirectory 'live_search.enabled'

if ([string]::IsNullOrWhiteSpace($env:TAVILY_API_KEY)) {
    throw 'TAVILY_API_KEY is not available in this session. No credential was written.'
}

New-Item -ItemType Directory -Path $credentialDirectory -Force | Out-Null
$secureKey = ConvertTo-SecureString $env:TAVILY_API_KEY -AsPlainText -Force
$secureKey | ConvertFrom-SecureString | Set-Content -LiteralPath $credentialPath -Encoding UTF8
'enabled' | Set-Content -LiteralPath $enabledPath -Encoding ASCII

[pscustomobject]@{
    Status = 'LIVE_SEARCH_CREDENTIAL_ENCRYPTED_FOR_CURRENT_WINDOWS_USER'
    CredentialDisplayed = $false
    GitIgnoredRuntimeLocation = $true
}

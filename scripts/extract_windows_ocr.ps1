param(
    [Parameter(Mandatory=$true)][string]$ImagePath,
    [Parameter(Mandatory=$true)][string]$OutputPath,
    [string]$Language = 'en-US'
)
$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$inputFile = [IO.Path]::GetFullPath((Join-Path $workspace $ImagePath))
$outputFile = [IO.Path]::GetFullPath((Join-Path $workspace $OutputPath))
$prefix = $workspace.TrimEnd('\') + '\'
foreach ($path in @($inputFile, $outputFile)) {
    if (-not $path.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'OCR paths must stay inside the workspace.'
    }
}
if (-not (Test-Path -LiteralPath $inputFile -PathType Leaf)) { throw 'Input image not found.' }
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.FileAccessMode,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.SoftwareBitmap,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrResult,Windows.Foundation,ContentType=WindowsRuntime]
$null = [Windows.Globalization.Language,Windows.Globalization,ContentType=WindowsRuntime]
$asyncMethod = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.IsGenericMethodDefinition -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
} | Select-Object -First 1
function Await-OcrOperation($Operation, [Type]$ResultType) {
    $task = $asyncMethod.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.GetAwaiter().GetResult()
}
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new($Language))
if ($null -eq $engine) { throw "OCR language unavailable: $Language" }
$file = Await-OcrOperation ([Windows.Storage.StorageFile]::GetFileFromPathAsync($inputFile)) ([Windows.Storage.StorageFile])
$stream = Await-OcrOperation ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
try {
    $decoder = Await-OcrOperation ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Await-OcrOperation ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    try {
        if ($bitmap.PixelWidth -gt [Windows.Media.Ocr.OcrEngine]::MaxImageDimension -or
            $bitmap.PixelHeight -gt [Windows.Media.Ocr.OcrEngine]::MaxImageDimension) { throw 'Image exceeds OCR size limit.' }
        $result = Await-OcrOperation ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
        $lines = @($result.Lines | ForEach-Object {
            @{ text = $_.Text; words = @($_.Words | ForEach-Object {
                @{ text = $_.Text; x = $_.BoundingRect.X; y = $_.BoundingRect.Y;
                   width = $_.BoundingRect.Width; height = $_.BoundingRect.Height }
            }) }
        })
        $hasher = [Security.Cryptography.SHA256]::Create()
        try { $imageHash = [BitConverter]::ToString($hasher.ComputeHash([IO.File]::ReadAllBytes($inputFile))).Replace('-', '').ToLowerInvariant() }
        finally { $hasher.Dispose() }
        $report = @{ schema_version = 1; engine = 'WINDOWS_OCR'; language = $Language;
            input_sha256 = $imageHash;
            image_width = $bitmap.PixelWidth; image_height = $bitmap.PixelHeight;
            extracted_at = [DateTimeOffset]::UtcNow.ToString('o'); lines = $lines;
            status = 'OCR_CANDIDATES_PENDING_RECONCILIATION'; creates_approved_facts = $false;
            changes_verdict = $false; network_used = $false }
        $directory = Split-Path -Parent $outputFile
        [IO.Directory]::CreateDirectory($directory) | Out-Null
        [IO.File]::WriteAllText($outputFile, ($report | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))
        Write-Output "OCR completed: $($lines.Count) lines. No facts approved."
    } finally { if ($bitmap) { $bitmap.Dispose() } }
} finally { $stream.Dispose() }

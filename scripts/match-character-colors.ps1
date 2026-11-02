param(
    [Parameter(Mandatory=$true)][string]$ReferencePath,
    [Parameter(Mandatory=$true)][string]$OutputPath,
    [Parameter(Mandatory=$true)][string]$MaskPath,
    [string]$InputPath = (Join-Path $PSScriptRoot '../assets/characters/first-character/concepts/turnaround-v02-accessories-v10.png'),
    [switch]$BrightenWhites
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$references = @([System.Drawing.Bitmap].Assembly.Location,
    [System.Drawing.Rectangle].Assembly.Location,
    [System.Runtime.InteropServices.Marshal].Assembly.Location,
    [System.Text.StringBuilder].Assembly.Location,
    (Join-Path $PSHOME 'System.Private.Windows.GdiPlus.dll'),
    (Join-Path $PSHOME 'System.Private.Windows.Core.dll'),
    (Join-Path $PSHOME 'System.Runtime.dll'),
    [object].Assembly.Location) | Select-Object -Unique
Add-Type -Path (Join-Path $PSScriptRoot 'match-character-colors.cs') -ReferencedAssemblies $references
$method = if ($BrightenWhites) { 'BrightenWhites' } else { 'Run' }
$result = [CharacterColorMatch]::$method([System.IO.Path]::GetFullPath($InputPath),
    [System.IO.Path]::GetFullPath($ReferencePath), [System.IO.Path]::GetFullPath($OutputPath),
    [System.IO.Path]::GetFullPath($MaskPath)) | ConvertFrom-Json
$verification = [CharacterColorMatch]::Verify([System.IO.Path]::GetFullPath($InputPath),
    [System.IO.Path]::GetFullPath($OutputPath), [System.IO.Path]::GetFullPath($MaskPath)) | ConvertFrom-Json
$result | Add-Member -NotePropertyName verification -NotePropertyValue $verification
$result | ConvertTo-Json -Depth 6

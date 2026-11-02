param(
    [string]$InputPath = (Join-Path $PSScriptRoot '../assets/characters/first-character/concepts/turnaround-v02-accessories-v08.png'),
    [string]$OutputPath = (Join-Path $PSScriptRoot '../assets/characters/first-character/concepts/turnaround-v02-accessories-v09.png'),
    [string]$SkinReferencePath = ''
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$references = @([System.Drawing.Bitmap].Assembly.Location,
    [System.Drawing.Rectangle].Assembly.Location,
    [System.Runtime.InteropServices.Marshal].Assembly.Location,
    [System.Threading.Tasks.Parallel].Assembly.Location,
    [System.Collections.Generic.Queue[int]].Assembly.Location,
    [System.Runtime.GCSettings].Assembly.Location,
    (Join-Path $PSHOME 'System.Private.Windows.GdiPlus.dll'),
    (Join-Path $PSHOME 'System.Private.Windows.Core.dll'),
    (Join-Path $PSHOME 'System.Collections.dll'),
    (Join-Path $PSHOME 'System.Runtime.dll'),
    [object].Assembly.Location) | Select-Object -Unique
Add-Type -Path (Join-Path $PSScriptRoot 'denoise-character.cs') -ReferencedAssemblies $references
[CharacterDenoise]::Run([System.IO.Path]::GetFullPath($InputPath), [System.IO.Path]::GetFullPath($OutputPath), $SkinReferencePath)

param([Parameter(Mandatory=$true)][string]$TextPath,[Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference='Stop'
$voice=New-Object -ComObject SAPI.SpVoice
$stream=New-Object -ComObject SAPI.SpFileStream
try {
    $german=$voice.GetVoices('Language=407')
    if($german.Count -eq 0){throw 'Keine deutsche SAPI-Stimme installiert.'}
    $voice.Voice=$german.Item(0)
    $voice.Rate=0
    $stream.Open($OutputPath,3,$false)
    $voice.AudioOutputStream=$stream
    [void]$voice.Speak([System.IO.File]::ReadAllText($TextPath),0)
} finally {
    $stream.Close()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($stream)
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($voice)
}

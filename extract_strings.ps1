$bytes = [System.IO.File]::ReadAllBytes('haian_image.jpg')
$text = [System.Text.Encoding]::ASCII.GetString($bytes)
$matches = [regex]::Matches($text, '(http|ftp|mail|@|\.com|\.de|\.org|hack|puzzle|challenge|key|password|flag)')
if ($matches.Count -gt 0) {
    Write-Host "Found matches:"
    $matches | ForEach-Object { Write-Host $_.Value }
} else {
    Write-Host "No obvious matches found"
}

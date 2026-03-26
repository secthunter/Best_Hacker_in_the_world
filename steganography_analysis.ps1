# Steganography and hidden data analysis for haian.de investigation

# Load the image
$imagePath = "haian_image.jpg"
$imageBytes = [System.IO.File]::ReadAllBytes($imagePath)

Write-Host "=== BASIC IMAGE ANALYSIS ==="
Write-Host "File size: $($imageBytes.Length) bytes"

# Check for common steganography signatures
Write-Host "`n=== STEGANOGRAPHY SIGNATURES ==="

# Look for potential LSB (Least Significant Bit) patterns
$lsbCount = 0
for ($i = 0; $i -lt [Math]::Min(1000, $imageBytes.Length); $i++) {
    if ($imageBytes[$i] % 2 -eq 1) {
        $lsbCount++
    }
}
Write-Host "LSB analysis (first 1000 bytes): $lsbCount odd bytes out of 1000"

# Look for repeated patterns that might indicate hidden data
Write-Host "`n=== PATTERN ANALYSIS ==="
$patterns = @{}
for ($i = 0; $i -lt $imageBytes.Length - 3; $i++) {
    $pattern = "$($imageBytes[$i]),$($imageBytes[$i+1]),$($imageBytes[$i+2]),$($imageBytes[$i+3])"
    if ($patterns.ContainsKey($pattern)) {
        $patterns[$pattern]++
    } else {
        $patterns[$pattern] = 1
    }
}

$topPatterns = $patterns.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 5
Write-Host "Top 5 most common 4-byte patterns:"
foreach ($pattern in $topPatterns) {
    Write-Host "  $($pattern.Key): $($pattern.Value) occurrences"
}

# Extract and analyze any text data
Write-Host "`n=== EXTRACTED TEXT DATA ==="
$textData = [System.Text.Encoding]::ASCII.GetString($imageBytes)
$textData = $textData -replace '[^\x20-\x7E]', '' # Keep only printable ASCII

if ($textData.Length -gt 0) {
    Write-Host "Extracted ASCII text (first 500 chars):"
    Write-Host $textData.Substring(0, [Math]::Min(500, $textData.Length))
    
    # Look for potential coordinates, numbers, or codes
    $numbers = [regex]::Matches($textData, '\d+')
    if ($numbers.Count -gt 0) {
        Write-Host "`nFound numbers:"
        $numbers | ForEach-Object { Write-Host "  $($_.Value)" }
    }
    
    # Look for potential base64-like strings
    $base64Pattern = '[A-Za-z0-9+/]{20,}={0,2}'
    $base64Matches = [regex]::Matches($textData, $base64Pattern)
    if ($base64Matches.Count -gt 0) {
        Write-Host "`nPotential base64 strings:"
        $base64Matches | ForEach-Object { Write-Host "  $($_.Value)" }
    }
} else {
    Write-Host "No readable ASCII text found in image data"
}

# Check EXIF data if this were a real image analysis
Write-Host "`n=== METADATA ANALYSIS ==="
Write-Host "Note: Full EXIF analysis would require specialized tools"
Write-Host "Image dimensions: 700x1000 (from HTTP headers)"

Write-Host "`n=== NEXT STEPS FOR INVESTIGATION ==="
Write-Host "1. Use specialized steganography tools (steghide, outguess)"
Write-Host "2. Analyze image with hex editors for hidden data"
Write-Host "3. Check for LSB encoding in image pixels"
Write-Host "4. Look for frequency analysis patterns"
Write-Host "5. Cross-reference with other haian.de related materials"

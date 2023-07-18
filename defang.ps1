function Defang-URL {
    param (
        [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
        [string]$URL
    )

    # Replace colon (:) with textual representation (colon)
    $defangedURL = $URL -replace ':', '(:)'

    # Replace dot (.) with textual representation (dot)
    $defangedURL = $defangedURL -replace '\.', '(dot)'

    # Replace slashes (/) with textual representation (slash)
    $defangedURL = $defangedURL -replace '/', '/'

    # Replace square brackets with textual representations
    $defangedURL = $defangedURL -replace '\[', '['
    $defangedURL = $defangedURL -replace '\]', ']'

    return $defangedURL
}

# Check if there are command-line arguments
if ($args.Count -gt 0) {
    $originalURL = $args[0]
}
else {
    # If no command-line arguments, read from clipboard
    $originalURL = Get-Clipboard
}

# Check if the clipboard contains a URL
if ([string]::IsNullOrWhiteSpace($originalURL)) {
    Write-Host "No URL found in the clipboard."
}
else {
    $defangedURL = Defang-URL -URL $originalURL
    Write-Host "Defanged URL: $defangedURL"
}

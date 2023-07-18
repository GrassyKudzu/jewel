function Defang-Url {
    param(
        [string]$url
    )

    # Replace ':' with 'x' and '.' with '[.]'
    $defangedUrl = $url -replace ':', 'x' -replace '\.', '[.]'
    return "h$defangedUrl"
}

function Get-InputUrl {
    param(
        [string]$url
    )

    if (-not $url) {
        $clipboardContent = Get-Clipboard
        if ($clipboardContent) {
            return $clipboardContent.Trim()
        } else {
            Write-Host "No URL provided, and the clipboard is empty."
            exit 1
        }
    }

    return $url.Trim()
}

function Test-DefangUrl {
    param(
        [string]$inputUrl,
        [string]$expectedResult
    )

    $defangedUrl = Defang-Url -url $inputUrl
    $isEqual = $defangedUrl -eq $expectedResult

    Write-Host "Testing Defang-Url:"
    Write-Host "Input URL: $inputUrl"
    Write-Host "Defanged URL: $defangedUrl"
    Write-Host "Expected Result: $expectedResult"
    Write-Host "Test Result: $($isEqual -as [string])"
    Write-Host ""
}

# Test cases
Test-DefangUrl -inputUrl "https://www.example.com" -expectedResult "hxxps://www[.]example[.]com"
Test-DefangUrl -inputUrl "http://example.org/something?param=value" -expectedResult "hxxp://example[.]org/something?param=value"
Test-DefangUrl -inputUrl "ftp://ftp.example.com" -expectedResult "hftp://ftp[.]example[.]com"
Test-DefangUrl -inputUrl "file://shared/files/document.txt" -expectedResult "hfile://shared/files/document[.]txt"

# Get the URL from the command-line argument or clipboard
$normalUrl = Get-InputUrl -url $args[0]
$defangedUrl = Defang-Url -url $normalUrl
Write-Host "DEFANGED URL: $defangedUrl"

param(
    [string]$url = ""
)

function Defang-Url {
    param(
        [string]$url
    )

    $defangedUrl = $url -replace ":", "x" -replace "\.", "[.]"
    return "h" + $defangedUrl
}

function Get-InputUrl {
    if ($url -ne "") {
        return $url.Trim()
    } else {
        $clipboardContent = Get-Clipboard
        if ($clipboardContent) {
            return $clipboardContent.Trim()
        } else {
            Write-Host "No URL provided, and the clipboard is empty."
            exit 1
        }
    }
}

$normalUrl = Get-InputUrl
$defangedUrl = Defang-Url -url $normalUrl
Write-Host "DEFANGED URL: $defangedUrl"

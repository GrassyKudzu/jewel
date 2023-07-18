function Defang-Url {
    param (
        [string]$url
    )

    $periodCount = $url.Split('.').Length - 1
    if ($periodCount -eq 1) {
        $url = $url -replace '\.', '[.]'
    }
    elseif ($periodCount -eq 2) {
        $firstPeriodIndex = $url.IndexOf('.')
        $secondPeriodIndex = $url.IndexOf('.', $firstPeriodIndex + 1)

        if ($firstPeriodIndex -ne -1 -and $secondPeriodIndex -ne -1) {
            $url = $url.Substring(0, $firstPeriodIndex) + '[.' + $url.Substring($firstPeriodIndex + 1, $secondPeriodIndex - $firstPeriodIndex - 1) + '.]' + $url.Substring($secondPeriodIndex + 1)
        }
    }

    return $url
}

function Modify-Protocol {
    param (
        [string]$url
    )

    if ($url -match '^http://') {
        $url = $url -replace '^http://', 'hxxp://'
    }
    elseif ($url -match '^https://') {
        $url = $url -replace '^https://', 'hxxps://'
    }
    elseif ($url -match '^ftp://') {
        $url = $url -replace '^ftp://', 'fxp://'
    }
    elseif ($url -match '^file://') {
        $url = $url -replace '^file://', 'fxxe://'
    }

    return $url
}

if ($args.Length -ne 1) {
    Write-Host "Usage: powershell script.ps1 <URL>"
    exit 1
}

$normalUrl = $args[0]
$safeUrl = Modify-Protocol -url $normalUrl
$defangedUrl = Defang-Url -url $safeUrl
Write-Host "SAFE DEFANGED URL: $defangedUrl"

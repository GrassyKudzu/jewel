function Defang-Url {
    param(
        [string]$url
    )

    $firstPeriodIndex = $url.IndexOf('.')
    if ($firstPeriodIndex -ne -1) {
        $url = $url.Substring(0, $firstPeriodIndex) + '[.' + $url.Substring($firstPeriodIndex + 1)

        $secondPeriodIndex = $url.IndexOf('.', $firstPeriodIndex + 2)
        if ($secondPeriodIndex -ne -1) {
            $url = $url.Substring(0, $secondPeriodIndex) + '.]' + $url.Substring($secondPeriodIndex + 1)
        }
    }

    return $url
}

function Modify-Protocol {
    param(
        [string]$url
    )

    $url = $url -replace '^http://', 'hxxp://'
    $url = $url -replace '^https://', 'hxxps://'
    $url = $url -replace '^ftp://', 'fxp://'
    $url = $url -replace '^file://', 'fxxe://'

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

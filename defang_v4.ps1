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

if ($args.Length -ne 1) {
    Write-Host "Usage: powershell script.ps1 <URL>"
    exit 1
}

$normalUrl = $args[0]
$defangedUrl = Defang-Url -url $normalUrl
Write-Host "DEFANGED URL: $defangedUrl"

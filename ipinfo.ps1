import requests
import json
import argparse
import curses

VIRUSTOTAL_API_KEY = ""
SHODAN_API_KEY = ""

function Get-VirusTotalInfo {
    param (
        [Parameter(Mandatory = $true)]
        [string] $Query
    )

    $Url = "https://www.virustotal.com/api/v3/ip_addresses/$Query"
    $Headers = @{
        'x-apikey' = $VirusTotalApiKey
        'Content-Type' = 'application/json'
    }

    $Response = Invoke-RestMethod -Uri $Url -Headers $Headers -Method Get

    if ($Response.StatusCode -eq 200) {
        return $Response | ConvertTo-Json -Depth 4
    } else {
        return "VirusTotal API Error: $($Response.StatusCode)"
    }
}

function Get-ShodanInfo {
    param (
        [Parameter(Mandatory = $true)]
        [string] $Query
    )

    $Url = "https://api.shodan.io/shodan/host/$Query?key=$ShodanApiKey"
    $Response = Invoke-RestMethod -Uri $Url -Method Get

    if ($Response.StatusCode -eq 200) {
        return $Response | ConvertTo-Json -Depth 4
    } else {
        return "Shodan API Error: $($Response.StatusCode)"
    }
}

function Display-TUI {
    param (
        [Parameter(Mandatory = $true)]
        [string] $VirusTotalResult,

        [Parameter(Mandatory = $true)]
        [string] $ShodanResult
    )

    $Window = New-Object System.Management.Automation.Host.PSHostUserInterface -ArgumentList $Host

    $Window.Clear()

    $Window.WriteLine("=== VirusTotal Results ===")
    $Window.WriteLine($VirusTotalResult)

    $Window.WriteLine()
    $Window.WriteLine("=== Shodan Results ===")
    $Window.WriteLine($ShodanResult)

    $Window.ReadLine() | Out-Null
}

# Main script logic
try {
    $VirusTotalResult = Get-VirusTotalInfo -Query $Query
    $ShodanResult = Get-ShodanInfo -Query $Query

    Display-TUI -VirusTotalResult $VirusTotalResult -ShodanResult $ShodanResult
}
catch {
    Write-Host "An error occurred: $_"
}

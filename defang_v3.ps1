<#
.Synopsis
   This script defangs URLs
   defang.ps1
.DESCRIPTION
   This defangs URLs for sharing safely. 
.EXAMPLE
   defang.ps1 https://www.thhgttg.com
.INPUTS
   An argument can be provided on the keyboard or if not the clipboard is read. 
.OUTPUTS
   Output from this cmdlet (if any)
.NOTES
   MIT License

  Copyright (c) 2023 Matthew J. Harmon

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
.FUNCTIONALITY
   This defangs URLs according to a minimalist approach. 
#>


Get-Help .\defang.ps1 -Full

# Results

<#

NAME
    D:\Scripts\defang.ps1
    
SYNOPSIS
    This defangs URLs
#>
function Defang-URL {
    param (
        [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
        [string]$URL
    )

    # Replace first colon (:) with textual representation [:]
    $defangedURL = $URL -replace '^([^:]+):', '$1[:]'

    # Replace subsequent colons (:) with textual representation [:]
    $defangedURL = $defangedURL -replace ':', '[:]', 1

    # Find the last period in the URL (TLD period) and replace it with textual representation (dot)
    $defangedURL = $defangedURL -replace '(\.[a-zA-Z]{2,})(/?|$)', '(dot)$1$2'

    # Surround the domain name with brackets [.slashdot.]
    $defangedURL = $defangedURL -replace '(https?://)(www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', '$1$2[.$3]'

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

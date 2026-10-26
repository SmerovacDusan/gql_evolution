<#
Skript ke generování UUID v PowerShellu.

Spuštění v terminalu:
PS C:\Cesta\K\Souboru\gql_evolution> .\uuid_generovani.ps1
#>

$pocet = Read-Host -Prompt "Zadej počet UUID k vygenerování"

for ($i=1; $i -le $pocet; $i++) {
    New-Guid
}
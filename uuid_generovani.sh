#!/bin/bash

# Skript pro generování UUID v bash
# 
# Spuštění v terminalu:
# user@computer:/Cesta/K/Souboru/gql_evolution$ ./uuid_generovani.sh

read -p "Zadej počet UUID k vygenerování: " pocet

for ((i=1; i<=$pocet; i++)); do
	uuidgen
done
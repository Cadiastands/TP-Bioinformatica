# TP Bioinformática
Tras clonar el repositorio, correr `pip install -r requirements.txt`

### Instrucciones para correr los scripts

-   Ejercicio 1: `python3 scripts/Ej1.py -input <input en formato GenBank> -output <nombre del output>`
    
-   Ejercicio 2: `python3 scripts/Ej2.py -input <input en formato GenBank> -output <nombre del output> [-mode BLAST MODE (local o remote)] [-db DB_PATH (requerido solo para modo local)]`\
    Previamente es necesario agregar al PATH la dirección al bin de blast, en caso de querer usar el modo local


### Archivos usados

- Gen fibrosis quistica: https://www.ncbi.nlm.nih.gov/gene/1080

- Transcript (ARNm): https://www.ncbi.nlm.nih.gov/nuccore/NM_000492.4

### Links utiles

- BLAST Job: https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&RID=KSED9631013
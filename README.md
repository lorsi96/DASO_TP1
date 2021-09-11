# Trabajo Práctico Número 1

## Instrucciones
Inicializar:
- El servidor, que recibe por UDP en formato .json información sobre los tipos de cambio y los muestra en consola.
- El cliente, que envía por UDP en formato .json la información sobre los tipos de cambio al servidor, leídas de un archivo .csv

La forma más simple de inicializar ambos es la siguiente:

```bash
python3 PizarraService.py  8080
python3 ParserService.py  --port 8080
```

### ParserService
Parser service lee desde un archivo `config.txt` el path a otro archivo `.csv` que contiene información de tipos de cambio. Dicha información es leída de forma periódica y reportada a `PizarraService` mediante UDP.

Parser service admite distintas configuraciones al ser ejecutado:
```
optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Directorio de un arhivo .txt con el path del archivo .csv con los
                   tipos de cambio
  --port PORT      Puerto en Localhost del servidor
  --period PERIOD  Tiempo en segundos entre cada refresco de dato (lectura del archivo de tipos de cambio)
```
El archivo `.csv` con los tipos de cambio debe tener una estructura similar al ejemplo a continuación

```csv
id,nombre,compra,venta
1,Dolar,58.63,61.61
2,Euro,65.12,68.93
3,Real,17.45,15.24
```


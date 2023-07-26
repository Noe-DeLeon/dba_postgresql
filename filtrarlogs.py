		#postgresql-2023-07-26_011840.log postgresql-2023-07-26_025419.log 
import sys
import time
import os
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

ruta_logs = sys.argv[1] if len(sys.argv) >= 2 else '/var/lib/postgresql/pgdata/log/postgresql-2023-07-26_011840.log'
filtro_logs = sys.argv[2] if len(sys.argv) == 3 else 'filtrologs.log'
filtros = ["ERROR", "FATAL", "PANIC", "WARNING"]

def filtrar_logs(logspsql, logsfiltrados):
    try:
        with open(logspsql, "r") as entrada, open(logsfiltrados, "w") as salida:
            os.system("clear")
            for linea in entrada:
                if any(palabra in linea for palabra in filtros):
                    salida.write(linea)
                    print(color_texto(linea), end='')
    except FileNotFoundError:
        print("Archivo de logs no encontrado")

def color_texto(texto):
    colores = {
        "ERROR": 31,    # Rojo
        "FATAL": 35,    # Magenta
        "PANIC": 34,     # Azul
        "WARNING": 33   # Amarillo
    }

    expresion_regular = re.compile(r'\b(' + '|'.join(re.escape(palabra) for palabra in colores.keys() if palabra.isupper()) + r')\b')
    texto_resaltado = expresion_regular.sub(lambda match: f"\033[{colores[match.group(0)]}m{match.group(0)}\033[0m", texto)
    return texto_resaltado

class ModificacionLogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == ruta_logs:
            filtrar_logs(ruta_logs, filtro_logs)

if __name__ == "__main__":
    filtrar_logs(ruta_logs, filtro_logs)
    event_handler = ModificacionLogHandler()
    observer = Observer()
    observer.schedule(event_handler, path=ruta_logs, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()	


import paramiko
import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Datos de conexión al servidor
hostname = '192.168.11.198'
port = 22
username = 'epidater'
password = 'r00t&4ss'
mule_ee_path = '/home/epidater/scripting/mule_ee.log'
mule_agent_path = '/home/epidater/scripting/mule_agent.log'

# Directorio de destino en tu computadora local
local_backup_dir = os.path.expanduser(r'~/Desktop/192.168.11.198')

# Crear el directorio de backup si no existe
if not os.path.exists(local_backup_dir):
    os.makedirs(local_backup_dir)

def descargar_logs():
    try:
        # Crear una conexión SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username, password)

        # Usar SFTP para descargar el archivo de logs
        sftp = client.open_sftp()
        timestamp = datetime.now().strftime('%d.%m.%Y_%H.%M.%S')
        local_mule_ee = os.path.join(local_backup_dir, f'mule_ee_{timestamp}.txt')
        local_mule_agent = os.path.join(local_backup_dir, f'mule_agent_{timestamp}.txt')
        sftp.get(mule_ee_path, local_mule_ee)
        sftp.get(mule_agent_path, local_mule_agent)
        sftp.close()
        client.close()

        print(f'Log file desde {mule_ee_path} ha sido respaldado a {local_mule_ee}')
        print(f'Log file desde {mule_agent_path} ha sido respaldado a {local_mule_agent}')
        
        buscar_errores(local_mule_ee, os.path.join(local_backup_dir, f'ERRORES_mule_ee_{timestamp}.txt'))
        buscar_errores(local_mule_agent, os.path.join(local_backup_dir, f'ERRORES_mule_agent_{timestamp}.txt'))

    except paramiko.SSHException as e:
        print(f"Error al conectar o durante la transferencia de archivos: {e}")

def buscar_errores(archivo_log, archivo_errores):
    try:
        with open(archivo_log, 'r') as log:
            errores = [linea for linea in log if 'ERROR' in linea]
        
        if errores:
            with open(archivo_errores, 'w') as error_file:
                error_file.writelines(errores)
            print(f'Errores encontrados en {archivo_log} se han guardado en {archivo_errores}')
        else:
            print(f'No se encontraron errores en {archivo_log}')
    
    except IOError as e:
        print(f"Error al leer o escribir archivos: {e}")

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('mule_ee.log') or event.src_path.endswith('mule_agent.log'):
            print(f'Archivo modificado: {event.src_path}')
            buscar_errores(event.src_path, os.path.join(local_backup_dir, f'ERRORES_{os.path.basename(event.src_path)}'))

# Sincronizar archivos remotos a intervalos regulares
def sincronizar_archivos(intervalo_segundos):
    while True:
        descargar_logs()
        time.sleep(intervalo_segundos)

# Configurar el observador
event_handler = LogHandler()
observer = Observer()
observer.schedule(event_handler, path=local_backup_dir, recursive=False)
observer.start()

try:
    # Sincronizar archivos cada 60 segundos
    sincronizar_archivos(60)
except KeyboardInterrupt:
    observer.stop()
observer.join()








# por Marcos Olazar para Epidata :)

################################
####### Respaldar logs  ########
################################

import paramiko
import os
from datetime import datetime

# Datos de conexión al servidor
hostname = '192.168.11.198'
port = 22
username = 'epidater'
password = 'r00t&4ss'
mule_ee_path = '/home/epidater/scripting/mule_ee.log'
mule_agent_path = '/home/epidater/scripting/mule_agent.log'

# Directorio de destino en tu computadora local
local_backup_dir = os.path.expanduser('~/Desktop/192.168.11.198')

# Crear el directorio de backup si no existe
if not os.path.exists(local_backup_dir):
    os.makedirs(local_backup_dir)

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


################################
##### Buscador de errores ######
################################

def buscar_errores(archivo_log, archivo_errores):
    with open(archivo_log, 'r') as log:
        lineas = log.readlines()
    
    errores = [linea for linea in lineas if 'ERROR' in linea]
    
    if errores:
        with open(archivo_errores, 'w') as error_file:
            error_file.writelines(errores)
        print(f'Errores en encontrados en {archivo_log} se han guardado en {archivo_errores}')
    else:
        print(f'No se encontraron errores en {archivo_log}')

# Buscar errores en ambos archivos de log
archivo_errores_mule_ee = os.path.join(local_backup_dir, f'ERRORES_mule_ee_{timestamp}.txt')
archivo_errores_mule_agent = os.path.join(local_backup_dir, f'ERRORES_mule_agent_{timestamp}.txt')

buscar_errores(local_mule_ee, archivo_errores_mule_ee)
buscar_errores(local_mule_agent, archivo_errores_mule_agent)















# por Marcos Olazar para Epidata :)
# recolector_logs_servidor_ssh

[![.png](https://i.imgur.com/WnY0WRi.png)](https://i.imgur.com/WnY0WRi)


## Automatiza la recolección y detección de errores en .logs 

Busca y respalda archivos logs de servidores (SSH) al desktop, discriminando en el caso de que exista líneas de código con error.
El repositorio cuenta con dos versiones, una sin observador, compilarlo y ejecutar el .exe cada vez que desee usarlo.
Y la otra con la librería watchdog lo que permite que esté pendiente del servidor recolectando permanentemente en el caso de actualización de logs.

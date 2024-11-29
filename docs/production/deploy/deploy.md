**Importante:** Para que el proyecto pueda funcionar con supervisor, es necesario que este instalado gunicorn dentro del entorno del proyecto.

Tener a consideración estos "variables".:

- <server_host>: example_server - Nombre del Servidor.
- <project>: example - Nombre del proyecto en el repositorio de github.
- <private_ip_address>: IP privada del servidor. No la IP pública.
- <port>: Puerto donde se expondra el servicio
- <server_domain>: www.example.com - Dominio del Proyecto

# Supervisor

**1.-** Instalamos supervisor:

    sudo apt-get install supervisor

**2.-** Creamos el archivo de configuración dentro de la carpeta de supervisor:

	sudo nano /etc/supervisor/conf.d/<project>.conf

**3.-** Pegamos el contenido del archivo "supervisor.conf" de esta carpeta en el archivo creado con anterioridad. Recuerda que debes sustituir las variables que se encuentren en el archivo.

**4.-** Creamos el usuario que se necesita en el archivo de supervisor:

	useradd -s /sbin/nologin <user>

**5.-** Procedemos a reiniciar supervisor:

    sudo supervisorctl reread
    sudo supervisorctl update

De esta forma el servicio estara corriendo y puede comprobarse con:

	sudo supervisorctl status

# UWSGI

**1.-** Creamos el archivo uwsgi en la ruta del proyecto:

	nano /home/<server_host>/<project>/.config/environment/production/<project>_uwsgi.ini

Recuerda sustituir el texto "<project>"

**2.-** Pega el contenido del archivo uwsgi.ini de esta carpeta en el archivo creado con anterioridad, Recuerda quqe debes sustituir las variables que se encuentren en el archivo.

**3.-** Podemos probar el funcionamiento del proyecto:

	uwsgi --ini /home/<server_host>/<project>/.config/environment/production/<project>_uwsgi.ini

**4.-** Para que se mantenga activo siempre, procedemos a crearlo como servicio, para ello crearemos el siguiente archivo:

> Fuente: https://uwsgi-docs.readthedocs.io/en/latest/Systemd.html

	sudo nano /etc/systemd/system/<project>.service


**5.-** Iniciamos el servicio:

    sudo systemctl restart <project>

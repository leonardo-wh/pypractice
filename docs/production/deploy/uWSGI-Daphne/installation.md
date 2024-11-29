# Instalacion en produccion con uWSGI y Daphne

Estos pasos se ejecutan despues de instalar todos los requerimientos. Redis superior a 5, Supervisor, Nginx, uWSGI, Daphne

## 1. Instala lo necesario para hacer deploy

Actualiza tu entorno o instala Daphne (ya viene en el requirements.txt)

__1.1__ En requirements.txt agregar las siguintes dependencioas

````
channels==3.0.4
channels-redis==3.3.1
daphne="==3.0.2"
````

Una vez agregadas activar el entorno del proyecto y actualizar.
````
cd pypractice
pipenv shell
pipenv update
````

Por último agrega la ultima dependencia.

````
pip install -U 'Twisted[tls,http2]'
````

## 2. Correr workers con supervisor

### 2.1 Crear directorios para los logs
    
    mkdir /home/DjangoBase_Server/pypractice/.logs/celery/
    mkdir /home/DjangoBase_Server/pypractice/.logs/asgi/
    
    touch /home/DjangoBase_Server/pypractice/.logs/celery/pypractice_flower.log
    touch /home/DjangoBase_Server/pypractice/.logs/celery/pypractice_flower_error.log

    touch /home/DjangoBase_Server/pypractice/.logs/celery/pypractice_worker.log
    touch /home/DjangoBase_Server/pypractice/.logs/celery/pypractice_worker_error.log
    
    touch /home/DjangoBase_Server/pypractice/.logs/celery/pypractice.log
    touch /home/DjangoBase_Server/pypractice/.logs/celery/pypractice_error.log
    
    touch /home/DjangoBase_Server/pypractice/.logs/uwsgi/main_uwsgi.log
    touch /home/DjangoBase_Server/pypractice/.logs/asgi/asgi.log
    
### 2.2 Crear el archivo pypractice.conf para guardar la configuración de los workers.
Creamos el archivo pypractice.conf y copiamos la configuración del archivo __pypractice.conf__ ubicado en: __docs > production > deploy > uWSGI-Daphne > supervisor__ de este proyecto.
__NOTA__ cambiar rutas __command__ __directory__ __stderr_logfile__ __stderr_logfile__ __stderr_logfile__ __stderr_logfile__ que estan en el archivo por las rutas de tu proyecto.


```bash
sudo nano /etc/supervisor/conf.d/pypractice.conf
```

### 2.3 Reiniciar supervisor
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
```

### 2.4 Verificar el status de los workers.
Tras configurar los workers vericamos el status de nuestros workers.
```bash
sudo supervisorctl status
```
Deberiamos tener la siguiente salida.
```
cFlower                              RUNNING   pid 40532, uptime 0:00:37
cpypractice                         RUNNING   pid 40530, uptime 0:00:37
cpypracticeWorker                   RUNNING   pid 40531, uptime 0:00:37
```

Si en algún worker tuvieramos un error, podemos verificar los logs del worker que este fallando y poder solucionarlo dependiendo que muestre el error.
```bash
sudo tail -f 100 pypractice/.logs/celery/pypractice_flower_error.log
sudo tail -f 100 pypractice/.logs/celery/pypractice_error.log
sudo tail -f 100 pypractice/.logs/celery/pypractice_worker_error.log
```

## 3. Levantar el servicio con uWSGI

**1.-** Creamos el archivo uwsgi en la ruta del proyecto:
```
nano /home/DjangoBase_Server/pypractice/.config/environment/production/pypractice_uwsgi.ini
```

Recuerda sustituir el texto si es necesario
```
pypractice
DjangoBase_Server
```

**2.-** Pega el contenido del archivo **uwsgi.ini** de la carpeta **docs > production > deploy > ASGI-Daphne > pypractice_uwsgi** en el archivo creado con anterioridad, Recuerda que debes sustituir las variables que se encuentren en el archivo.

**3.-** Podemos probar el funcionamiento del proyecto:

    uwsgi --ini /home/DjangoBase_Server/pypractice/.config/environment/production/pypractice_uwsgi.ini

**4.-** Para que se mantenga activo siempre, procedemos a crearlo como servicio, para ello crearemos el siguiente archivo,
debe contener algo similar a **docs > production > deploy > uWSGI-Daphne > uwsgi > pypractice.service**:

> Fuente: https://uwsgi-docs.readthedocs.io/en/latest/Systemd.html

    sudo nano /etc/systemd/system/pypractice.service


**5.-** Iniciamos el servicio:

    sudo systemctl restart pypractice

## 4. Configurar NGINX

### 4.1. Crear directorios y archivos para almacenar los logs

```sh
sudo mkdir /etc/nginx/sites-enabled
sudo mkdir /etc/nginx/sites-available
sudo mkdir /home/DjangoBase_Server/pypractice/.logs/nginx
sudo touch /home/DjangoBase_Server/pypractice/.logs/nginx/pypractice.access.log
sudo touch /home/DjangoBase_Server/pypractice/.logs/nginx/pypractice.error.log
```

### 4.2. Editar el __nginx.conf__, copiar y pegar lo que contiene el archivo __nginx.conf__ ubicado en docs > production > deploy > uWSGI-Daphne > nginx > nginx.conf de este proyecto
```sh
sudo nano /etc/nginx/nginx.conf
```

### 4.3. Copiar la carpeta __h5bp__ al servidor

```sh
sudo scp -i ~/.ssh/<llave pem o publica> -r ~/Dropbox/Django/Bitol/Produccion/h5bp <usuario_de_tu_server>@<ip_de_tu_server>:/home/<usuario_de_tu_server>/h5bp
```
Ejemplo.

```sh
sudo scp -i ~/.ssh/pypractice.pem -r ~/Dropbox/Django/Bitol/Produccion/h5bp DjangoBase_Server@44.203.235.211:/home/DjangoBase_Server/h5bp
```

### 4.4. Copiar la carpta __h5bp__ al la carpta de nginx del servidor.
```
sudo cp -r /home/DjangoBase_Server/h5bp /etc/nginx
```

### 4.5. Si existe, cambiar el nombre del archivo __default.conf__ a __default.conf_back__
```
sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf_back
```

### 4.6. Reiniciar NGINX
```
sudo service nginx restart
```

## 5. Lenvar el servicio de ASGI con Daphne con servidor web NGINX.


### 5.1. Crear el archivo de configuración de NGINX.

```sh
sudo touch /etc/nginx/sites-available/pypractice
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/pypractice
```

### 5.2 . Configurar __pypractice__ en sites-available
Copiar y pegar lo que hay en el archivo __pypractice__ ubicado en __docs > production > deploy > uWSGI-Daphne > nignx__ de este proyecto
__NOTA__ cambiar rutas __alias__ __access_log__ __error_log__ que estan en el archivo por las rutas de tu proyecto.

```sh
sudo nano /etc/nginx/sites-available/pypractice
```
### Crear carpeta para los sockets
__5.3__ Cree el directorio de ejecución para los sockets a los que se hace referencia en el archivo de configuración del supervisor.
````
cd ~sudo mkdir /run/daphne/
sudo chmod -R 777 /run/daphne/
````
__5.4__ La carpeta /run/daphne/ se elimina cada vez que se reinicia el projecto, para evitar eso, creamos el archivo /usr/lib/tmpfiles.d/daphne.conf
````
touch /usr/lib/tmpfiles.d/daphne.conf
````
__5.5__ Agregamos lo siguiente a /usr/lib/tmpfiles.d/daphne.conf del paso anterior
````
d /run/daphne 0755
````

### 5.6. Configurar ASGI-Daphne en supervisor.
Este archivo ya existe porque en el paso 8.3 se creo para la configuración de los workers con supervisor, 
volvemos a editar el archivo de configuración con el siguiente comando.
```sh
sudo nano /etc/supervisor/conf.d/pypractice.conf
```
Al final de este archivo, copiar y pegar lo que hay en el archivo __asgi__ ubicado en __docs > production > deploy > ASGI-Daphne > supervisor__ de este proyecto
__NOTA__ cambiar rutas __directory__ __command__ __stdout_logfile__ que estan en el archivo por las rutas de tu proyecto.


### 5.7. Reiniciar NGINX y SUPERVISOR
```sh
Restart NGINX 
sudo nginx -t
sudo service nginx restart
sudo service nginx status
```
### 5.8. Reiniciar SUPERVISOR
```sh
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
sudo supervisorctl status
```
Se deberian agregar los siguientes servicios.
```
asgi:asgi0                       RUNNING   pid 43979, uptime 0:00:38
asgi:asgi1                       RUNNING   pid 43980, uptime 0:00:38
asgi:asgi2                       RUNNING   pid 43981, uptime 0:00:38
asgi:asgi3                       RUNNING   pid 43982, uptime 0:00:38
```

En caso de no estar corriendo estos servicios, podemos ver el error en el siguiente archivo, mostrara un salida igual a como se inicia un proyecto con runserver.
```sh
sudo tail -f 100 pypractice/.logs/asgi/asgi.log
```
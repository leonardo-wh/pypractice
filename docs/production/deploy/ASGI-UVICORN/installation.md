# Deploy proyecto ASGI con UVICORN.

## 1. Instalar redis.

__1.1__ Seguir los pasos de configuración del archivo __redis_conf.md__ ubicado en: __docs__ > __production__ > __deploy__ > __ASGI-UVICORN__ > __Redis__

Una vez realizado todos los pasos de configuración redis con nuestro proyecto que se indicaron en el paso 1.1. 
Verificamos lo siguiente.

__1.2__ Reinicia redis.

    sudo systemctl restart redis

__1.3__ En otra terminal redis

    redis-cli

Una vez estando dentro del cli de redis, nos autenticamos con nuestra password.

    127.0.0.1:6379> auth su_password_redis
    OK

Ejecutamos el comando PING.

    127.0.0.1:6379> PING

Deberias ver la siguiente salida, si es asi, todo esta correcto.

    Output:
    PONG

## 2. Instala lo necesario para hacer deploy

Actualiza tu entorno o instala Daphne (ya viene en el requirements.txt)

__2.1__ En requirements.txt agregar las siguintes dependencioas

````
channels = "==3.0.5"
channels-redis = "==3.4.1"
uvicorn = "==0.20.0"
django-widget-tweaks= "==1.4.12"
````

Una vez agregadas activar el entorno del proyecto y actualizar.
````
cd ~
cd pypractice
pipenv shell
pipenv update
````

 __NOTA__ Si te da error, trata de borrar el __Pipfile.lock__ e intenta de nuevo con los siguiente.

````
cd ~
cd pypractice
pipenv shell
pipenv install
````

Por último agrega la ultima dependencia.

````
pip install -U 'Twisted[tls,http2]'
pip install uvicorn[standard]
````

## 3 Instalar supervisor.

````
sudo apt-get install supervisor
````

__3.1__ Crear los directorios y archivos para almacenar los logs.

    mkdir/home/pypractice_server/pypractice/.logs/asgi/
    touch /home/pypractice_server/pypractice/.logs/asgi/asgi.log

## 4. Configuracion ASGI - Daphne con supervisorctl.

__4.1__ Crear el archivo de configuracion .conf de tu proyecto.

````
sudo nano /etc/supervisor/conf.d/pypractice.conf
````

Copiar y pegar lo que hay en el archivo __asgi_daphne_default__ ubicado en __docs__ > __production__ > __supervisor__ > __deploy__ > __ASGI-UVICORN__ > __Supervisor__ de este proyecto

__NOTA__ cambiar rutas __directory__ __command__ __stdout_logfile__ que estan en el archivo por las rutas de tu proyecto.

__4.2__ Reiniciar SUPERVISOR

```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
sudo supervisorctl status
```

Se deberian agregar los siguientes servicios.

    asgi:asgi0                       RUNNING   pid 43979, uptime 0:00:38
    asgi:asgi1                       RUNNING   pid 43980, uptime 0:00:38
    asgi:asgi2                       RUNNING   pid 43981, uptime 0:00:38
    asgi:asgi3                       RUNNING   pid 43982, uptime 0:00:38

En caso de no estar corriendo estos servicios, podemos ver los errores de django en el log que creamos en el paso __3.1__ Ejemplo.
```
sudo tail -f 100 /home/pypractice_server/pypractice/.logs/asgi/asgi.log
```

## 5. Configuración Nginx

__5.1__ Creamos el archivo nginx.list

```
sudo nano /etc/apt/sources.list.d/nginx.list
```

Pegamos lo siguiente:

    deb [arch=amd64] http://nginx.org/packages/mainline/ubuntu/ bionic nginx
    deb-src http://nginx.org/packages/mainline/ubuntu/ bionic nginx

__5.2__ Agregamos la llave
```
cd ~
wget http://nginx.org/keys/nginx_signing.key
sudo apt-key add nginx_signing.key
```

__5.3__ Actualizamos los paquetes e instalamos el nginx.

```
sudo apt-get update
sudo apt-get install nginx
```

__5.4__ Editar el __nginx.conf__ copiar y pegar lo que contiene el archivo __nginx_conf_default__ ubicado en __docs__ > __production__ > __Deploy__ > __ASGI-Daphne__ > __Nginx__ de este proyecto.

```
sudo nano /etc/nginx/nginx.conf
```

__5.5__ Copiar la carpeta __h5bp__ al servidor

__Nota__ La carpeta h5bp se encuentra en Dropbox de programadores, la idea importar esta carpeta en el servidor por medio de ssh.
```sh
sudo scp -i ~/.ssh/id_rsa -r ~/Dropbox/Django/Bitol/Produccion/h5bp pypractice_server@44.203.235.211:/home/pypractice_server/h5bp
```

__5.6__ Copiar la carpta __h5bp__ al la carpta de nginx del servidor.
```
sudo cp -r /home/pypractice_server/h5bp /etc/nginx
```

__5.7__ Cambiar el nombre del archivo __default.conf__ a __default.conf_back__
```
sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf_back
```

__5.8__ sudo service nginx restart.

```
sudo service nginx restart
```

__5.9__ Crear directorios configuracion y archivos para almacenar los logs.

-5.9.1 Crear logs __Nota__ Cambia la ruta de los logs con la ruta de tu proyecto de django.

        sudo mkdir /home/pypractice_server/pypractice/.logs/nginx
        sudo touch /home/pypractice_server/pypractice/.logs/nginx/pypractice.access.log
        sudo touch /home/pypractice_server/pypractice/.logs/nginx/pypractice.error.log

-5.9.2 Crear Carpetas de configuracion

        cd ~
        sudo mkdir /etc/nginx/sites-enabled
        sudo mkdir /etc/nginx/sites-available

-5.9.3 Crear el archivo de configuración de NGINX. __Nota__ Remplazar hunabku  por el nombre de tu proyecto.

      sudo touch /etc/nginx/sites-available/pypractice
      cd /etc/nginx/sites-enabled
      sudo ln -s ../sites-available/pypractice

-5.9.4 Editar nuestro archivo de nginx para el proyecto.

```
sudo nano /etc/nginx/sites-available/pypractice
```

Copiar y pegar lo que hay en el archivo __nginx_project_default__ ubicado en __docs__ > __production__ > __Deploy__ > __ASGI-UVICORN__ > __Nginx__ de este proyecto.

__NOTA__ Cambiar rutas __server unix__ __alias__ __ssl_certificate__ __ssl_certificate_key__ __access_log__ __error_log__ que estan en el archivo por las rutas de tu proyecto.

## CLOUFLARE.
En el archivo nginx se agregan 2 certicados para el cifrado ssl del proyecto.

En el siguiente link: https://github.com/desarrollowh/pypractice/tree/master/docs/production/deploy/CloudFlare

Hay 2 formas de crear los certicados ssl.

- Forma 1: Certificados proporcionados por cloudflare: https://github.com/desarrollowh/pypractice/blob/master/docs/production/deploy/CloudFlare/forma_1_certificados_por_cloudflare.md
- Forma 2: Certiciados firmados por otra compania certificadora (Si queremos que el ssl este al nombre del dominio): https://github.com/desarrollowh/pypractice/blob/master/docs/production/deploy/CloudFlare/forma_2_crear_y_firmar_certificados.md


## 7. Reiniciar nginx.

```
sudo nginx -t
sudo service nginx reload
sudo service nginx restart
sudo service nginx status
```

### 8. Reiniciar SUPERVISOR

```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
sudo supervisorctl status
```

Se deberian mostrar la siguiente salida.

        asgi:asgi0    RUNNING   pid 43979, uptime 0:00:38
        asgi:asgi1    RUNNING   pid 43980, uptime 0:00:38
        asgi:asgi2    RUNNING   pid 43981, uptime 0:00:38
        asgi:asgi3    RUNNING   pid 43982, uptime 0:00:38

En caso de no estar corriendo estos servicios, podemos ver el error en el log que se creo en el paso 3.1, mostrara un salida igual a como se inicia un proyecto con runserver.

```
sudo tail -f 100 /home/pypractice_server/pypractice/.logs/asgi/asgi.log
```

### 8. TEST
Para comprobar el funcionamiento ingresamos a nuestro proyecto desde el navegador.
    
    djangobase.net

El test es sencillo, es una sala de chat donde ingresas un nombre y los mensajes que escribas se deben de pintar los mensajes.

# Introducción.
Este manual de instalación cuenta con 2 partes.

__1.__ La primera parte se explicara todo lo necesario a configurar en el server antes de lanzar a producción.

__2.__ En la segunda parte se elegirá un app server para lanzar el proyecto a producción, existen diferentes apps servers. Cada una contara con su manual de instalacion. 
 
- 1. __UWSGI__
- 2. __ASGI con Daphe__: Daphne es un servidor de protocolo HTTP, HTTP2 y WebSocket para ASGI y ASGI-HTTP, desarrollado para potenciar los canales de Django.
- 3. __ASGI con Uvicorn__
- 4. __UWSGI para HTTP + UVICORN o Daphne para Websocket (Django-Channels)__


## PARTE 1 - Instalacion requerimientos basicos.

### 1.- Crear el usuario del proyecto y eliminar el usuario ubuntu/root
Estos pasos se realizan despues de agregar el id_rsa o el pem para acceder al servidor.

__1.1__ Crear nuevo usuario dentro de la instancia

> Fuente1: https://aws.amazon.com/es/premiumsupport/knowledge-center/new-user-accounts-linux-instance/

> Fuente2: https://unix.stackexchange.com/a/293789

Creamos el nuevo usuario. Este usuario tiene que ir con siguiente sisntaxis: **nombreproyecto_server**. Ejemplo

```
sudo adduser pypractice_server
```

Agregamos al nuevo usuario al grupo sudo.

```
sudo usermod -aG sudo pypractice_server
```

__1.2__ Entramos con el nuevo usuario, creamos y asignamos permisos.

```
sudo su - pypractice_server
mkdir .ssh
chmod 700 .ssh
touch .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
```

__1.3__ En una terminal nueva, ingresaremos con el usuario __ubuntu__ o __root__ depende cual sea al usuario default y copiamos la key que hay en el archivo __authorized_keys__

```
cat ~/.ssh/authorized_keys
```

El contenido, lo agregaremos en el archivo authorized_keys del nuevo usuario __pypractice_server__

```
nano ~/.ssh/authorized_keys
```

__Nota:__ Tambien debes agregar tu llave id_rsa.pub de tu computadora esto para poder acceder sin el .pem

__1.4__ Configura el archivo config de tu computadora (local).

En otra terminal de tu computadora local edita el siguiente archivo.

```
nano ~/.ssh/config
```

y pega lo siguiente en tu archivo de conexiones por ssh.

```
Host TuServer-S1
    HostName <ip-server>
    User <el_nuevo_usuario_creado>
    Port <ssh-port-server>
    ForwardAgent yes
    IdentityFile <la_ruta_de_tu_.pem_o_llave_privada>
```

Ejemplo:

```
Host django-base-s1
 HostName 44.203.235.211
 Port 22
 User pypractice_server
 ForwardAgent yes
 IdentityFile ~/.ssh/id_rsa
```

Probamos que podamos conectarnos al servidor correctamente, en otra terminal ingresamos.
```
ssh django-base-s1
```
__Nota__ Con esto ya deberiamos haber ingresado con el nuevo usuario django-base-server

__1.5__ Borrar usuario default.

> Fuente: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/managing-users.html

__Nota__ Si el usuario default es root, no hace falta hacer este paso.

- En este caso el usuario default es: ubuntu
- El nuevo usuario principal es pypractice_server, que es el que se creo en el paso 1.1

Primero ya debimos haber entrado por ssh con el nuevo usuario, una vez dentro ejecutamos lo siguiente.

```
sudo userdel -r ubuntu
```

Verifica que ya no exista el usuario ubuntu. Al correr este comando ya no deberia aparecer el nombre del usuario ubuntu.

```
less /etc/passwd
```

### 2.- Instalar python 3.8.9 y otras dependencias.

__2.1__ Dependencias de ubuntu para el proyecto.

```
sudo apt-get update
# Este tal vez no sea necesario en ubuntu 20
sudo apt-get install build-essential libssl-dev libffi-dev python-dev 
sudo apt install python3-pip
sudo apt install -y python3-venv
sudo apt install gcc
sudo pip3 install pipenv
```

__Nota__ Si se presentan problemas con pip referente a dist-info correr lo siguiente y volver a correr los comandos.
```
sudo pip install --upgrade pip
sudo pip install --upgrade setuptools==58.3.0
sudo pip uninstall -y distro-info
sudo pip install distro-info==1.0
sudo apt-get remove --auto-remove python3-debian
```

__2.2__ Instalar paquetes de uwsgi.

```
sudo pip3 install uwsgi
```

__2.3__ Instalar Wkhtmltopdf.
Instalamos unzip
```
sudo apt install unzip
```

Descargar la ultima versión disponible de Wkhtmltopdf

```
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
```

Ejecutamos lo siguiente para Instalarlo.

```
sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
```

Nota: si marca un error de dependencias, tratar de instalar el ultimo que muestra en la lista del error.
    
> En caso de marcar dependencias incompletas ejecutar
>
> sudo apt --fix-broken install
>
> ejecutar nuevamente:
> 
> sudo dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb

__2.4__ Instalar Python 3

> En Ubuntu 20. por defecto ya esta python 3.8.10


Si se desea una versión de python diferente puede reemplazarse por el deseado.
```
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.8.9/Python-3.8.9.tgz
sudo tar zxvf Python-3.8.9.tgz
cd /usr/src/Python-3.8.9
sudo ./configure
sudo make
sudo make altinstall
```

### 3.- Clonar proyecto

__Nota__ Para tener permisos de clonar el proyecto ustedes deberian ser colaboradores en el proyecto a clonar,
y haber ingresado el ForwardAgent yes, de su llave privada id_rsa, el cual se explico en el paso __1.4__

```
cd ~
git clone git@github.com:desarrollowh/pypractice.git
```

Verifica que los archivos existan y estes en el ultimo commit.

### 4.- Configuración del entorno

__Nota__ Este paso es opcional, solo se indicara la ubicación donde se creara el entorno para el proyecto. 
Si no desea hacer esto puede omitir esto y seguir al paso 5.

```
sudo nano ~/.bashrc
```

Al final del archivo agregamos la variable WORKON_HOME con el valor de la ruta donde se creara el entorno.
Ejemplo:
    
    export WORKON_HOME=/var/waps/entornos

Guardamos y cerramos el archivo y aplicamos lo siguiente para aplicar cambios.

```
source ~/.bashrc
```

### 5.- Crear el entorno.

Debes posicionarte en la carpeta del proyecto y creamos la carpeta donde se ubicara nuestro entorno.

```
cd ~
cd pypractice
```

y ejecutar lo siguiente.
```
pipenv shell
```

Instalar las dependencias del proyecto. __Nota__ Las dependencias a instalar son las que estan definas en archivio Pipfile

```
pipenv install
```
Si todo fue exitoso, crea y edita el siguiente archivo y agrega tus variables de entorno necesarias para el funcionamiento de tu proyecto.
```
touch touch /home/pypractice_server/pypractice/.config/environment/production/.env
```

Editamos nuestro archivo .env 
```
nano  /home/pypractice_server/pypractice/.config/environment/production/.env
```
Y agregamos las siguientes variables

    DEBUG=1
    SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ALLOWED_HOSTS=127.0.0.1,*
    REDIS_DJANGO_WS_CHANNELS=redis://:@127.0.0.1:6379/0
    WS_SCHEME=ws

### 6.- Instalar PostgreSQL y crear la base de datos.

> Fuente: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04-es


__6.1__ Instalación

Ejecutamos lo siguiente para instalar la base de datos:

```
sudo apt install postgresql postgresql-contrib
```

__6.2__ Crear usuario

Ingresar al shell de postgres

```
sudo su - postgres
psql
```

Creamos el nombre de la bd, usuario y password para nuestra bd del proyecto. 

```
CREATE USER pypractice WITH PASSWORD 'xkpj@pypractice';
```

__6.3__ Crear base de datos

Ejecutamos lo siguiente:

```
CREATE DATABASE pypractice_bd;
```

Brindamos privilegios al usuario:

```
GRANT ALL PRIVILEGES ON DATABASE pypractice_bd TO pypractice;
```

__6.4__ Conectar nuestro proyecto con nuestra BD.

Editar nuestro archivo .env de producción.

```
cd ~
cd pypractice
sudo nano .config/environment/production/.env 
```
Agregamos las siguientes variables, los valores corresponden a tu nombre, usuario y contraseña de tu bd que creastes anteriormente.
```
DB_NAME=pypractice_bd
DB_USER=pypractice
DB_PASSWORD=xkpj@pypractice
DB_HOST=127.0.0.1
DB_PORT=5432
```

## 7.- Migraciones del Proyecto

Ingresamos a nuestro proyecto y activamos el entorno  y aplicamos las migraciones iniciales.

```bash
cd ~/pypractice
pipenv shell

python manage.py migrate_schemas --shared
python manage.py migrate_schemas
```

## 8.- Instalar redis

> Informacion obtenida de: https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04

```
sudo apt update
sudo apt install redis-server
```

__8.1__ Cambiamos el archivo de redis
    
    sudo nano /etc/redis/redis.conf

__8.2__ Buscamos con ctrl+w la linea que concuerde con "bind 127". Agregamos la ip privada del servidor

    # bind 127.0.0.1 IP_privada_server ejemplo: 
    bind 127.0.0.1 172.31.227.208

__8.3__ Si se desea asignar una contraseña, en una terminal aparte hacemos lo siguiente
    
    echo "tucontraseña" | sha1sum
    
    XXSWDb4FDSbFDdcSDS4dDS3Se44234a53e7e2e025dc5bde4XD12
    
__8.4__ En el archivo de redis.conf buscamos "requirepass", estara comentada. Cambiamos lo que tenia por la contraseña que se creo con anterioridad

    requirepass XXSWDb4FDSbFDdcSDS4dDS3Se44234a53e7e2e025dc5bde4XD12

__8.5__ Cerramos el documento y reiniciamos el servicio
    
    sudo service redis-server restart


__8.6__ Editar nuestras variables de productos .env de nuestro proyeto.

    sudo nano ~/pypractice/.config/environment/production/.env
    
-Buscar las siguientes variables (Si no las tiene, agregarlas).

    REDIS_DJANGO_WS_CHANNELS=redis://:<mipassword_redis>@127.0.0.1:6379/0
    
Ejemplo:

    REDIS_DJANGO_WS_CHANNELS=redis://:XXSWDb4FDSbFDdcSDS4dDS3Se44234a53e7e2e025dc5bde4XD12@127.0.0.1:6379/0


__8.7__ Reinicia redis. En otra terminal hacemos lo siguiente.

    sudo systemctl restart redis

__8.8__ Entramos al cli

    redis-cli

Una vez estando dentro del cli de redis, nos autenticamos con nuestra password.

    127.0.0.1:6379> auth su_password_redis
    OK

Ejecutamos el comando PING.

    127.0.0.1:6379> PING

Deberias ver la siguiente salida, si es asi, todo esta correcto.

    Output:
    PONG


### 9.- Instalar supervisor

```
sudo apt-get install supervisor
```

### 10. Instalar nginx

__10.1__ Creamos el archivo nginx.list
```
sudo nano /etc/apt/sources.list.d/nginx.list
```

Pegamos lo siguiente:
```
deb [arch=amd64] http://nginx.org/packages/mainline/ubuntu/ bionic nginx
deb-src http://nginx.org/packages/mainline/ubuntu/ bionic nginx
```

__10.2__  Agregamos la llave
```
cd ~
wget http://nginx.org/keys/nginx_signing.key
sudo apt-key add nginx_signing.key
```

__10.3__ Actualizamos los paquetes e instalamos el nginx.

```
sudo apt-get update
sudo apt-get install nginx
```

__10.4__ Configuramos el `NGINX`

Crear directorios y archivos para almacenar los logs

```
sudo mkdir /etc/nginx/sites-enabled
sudo mkdir /etc/nginx/sites-available

sudo mkdir /home/pypractice_server/pypractice/.logs/nginx
sudo touch /home/pypractice_server/pypractice/.logs/nginx/pypractice.access.log
sudo touch /home/pypractice_server/pypractice/.logs/nginx/pypractice.error.log
```

__10.5__ Editar el __nginx.conf__, copiar y pegar lo que contiene el archivo __nginx.conf_default__ ubicado en __docs__ > __production__ > __deploy__ > __nginx__ de este proyecto
```
sudo nano /etc/nginx/nginx.conf
```

__10.5__ Copiar la carpeta __h5bp__ al servidor

__Nota__ Este paso es tu computadora loca, en otra terminal.
```
sudo scp -i ~/.ssh/<llave pem o privada> -r ~/Dropbox/Django/Bitol/Produccion/h5bp <usuario_de_tu_server>@<ip_de_tu_server>:/home/<usuario_de_tu_server>/h5bp
```
Ejemplo.

```
sudo scp -i ~/.ssh/id_rsa -r ~/Dropbox/Django/Bitol/Produccion/h5bp pypractice_server@3.235.152.216:/home/pypractice_server/h5bp
```

__10.6__ Copiar la carpta __h5bp__ al la carpta de nginx del servidor.
Una ves se halla copiado esta carpeta en nuestro server, en otra terminal ingresamos en nuestro server y aplicamos lo siguiente.
```
sudo cp -r /home/pypractice_server/h5bp /etc/nginx
```

__10.7__ Cambiar el nombre del archivo __default.conf__ a __default.conf_back__
```
sudo mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf_back
```

__10.8__  Reiniciar NGINX
```
sudo service nginx restart
```

## Parte 2 - Deploy con app server.
Hasta este punto, ya hemos instalado todo lo necesario que el proyecto necesita.
Como siguiente paso se necesitara un app server para iniciar nuestro proyecto, a continuación puede usar cualquiera de estas cuatro opciones.

1. **UWSGI sin archivo .sock.**
    Manual de instalación: https://github.com/desarrollowh/pypractice/blob/master/docs/production/deploy/deploy.md


2. **ASIG con Daphne**:
    Manual de instalación en el archivo __installation.md__ ubicado en __docs__ > __production__ > __deploy__ >  __ASGI-Daphne__.

    Link: https://github.com/desarrollowh/pypractice/blob/master/docs/production/deploy/ASGI-Daphne/installation.md


3. **ASGI con Uvicorn**
    Manual de instalación en el archivo __installation.md__ ubicado en __docs__ > __production__ > __deploy__ >  __ASGI-UVICORN__.
    Link: https://github.com/desarrollowh/pypractice/blob/master/docs/production/deploy/ASGI-UVICORN/installation.md
   

4. **UWSGI para peticiones HTTP + UVICORN o Daphne para peticiones Websocket**
    Manual de instalación en el archivo __installation.md__ ubicado en __docs__ > __production__ > __deploy__ >  __uWSGI-Daphne__.
    Link: https://github.com/desarrollowh/pypractice/blob/master/docs/production/deploy/uWSGI-Daphne/installation.md


# Levantar el proyecto y servir los archivos media y static con Nginx

Tener a consideración estos "variables".:

- <server_host>: example_server - Nombre del Servidor
- <project>: example - Nombre del proyecto en el repositorio de github.
- <server_domain>: www.example.com - Dominio del Proyecto

Sustiya el valor en los archivos o en los comandos a continuación.
Tenga en cuenta que 

### Instalación

Para ello es necesario tener instalado nginx en el servidor.

**1.-** Ejecutamos en la terminal:

    sudo apt-get install nginx

**2.-** Crear directorios y archivos para almacenar los logs:

    sudo mkdir /etc/nginx/sites-enabled
    sudo mkdir /etc/nginx/sites-available
    sudo mkdir ~/<project>/.logs/nginx
    sudo touch  ~/<project>/.logs/nginx/<project>.access.log
    sudo touch  ~/<project>/.logs/nginx/<project>.error.log

**3.-** Editar el nginx.conf, copiar y pegar lo que contiene el archivo nginx.conf_default en esta ruta

    sudo nano /etc/nginx/nginx.conf

> Nota: Aqui se sustituye el usuario www-data por el usuario nginx.

**4.-** Crear archivo de configuracion:

    sudo touch /etc/nginx/sites-available/<project>
    cd /etc/nginx/sites-enabled
    sudo ln -s ../sites-available/<project>

**5.-** Copiamos el contenido del archivo "project" en esta ruta y lo pegamos como contenido del archivo que se acaba de crear. Recuerda sustituir los valores de cada variable dentro del archivo.

**6.-** Para efectuar los cambios debemos reiniciar nginx, pero es mejor primero comprobar que el archivo es correcto, para ello ejecuta:

	sudo nginx -t

Esto te mostrará los errores que se encuentren en el archivo.

**7.-** Reiniciar nginx

	sudo systemctl restart nginx



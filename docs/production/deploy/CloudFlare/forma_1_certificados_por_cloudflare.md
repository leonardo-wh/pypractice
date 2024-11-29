En el nginx hacemos referencia a los certicados ssl para que nuestro proyecto funcione con https.
En este paso. Ingresaremos a cloudflare y seleccionamos el dominio a configurar.

# 1. Crear certificados en Cloudflare

![0](https://user-images.githubusercontent.com/68970106/223751720-1bff61fe-1ff7-4ec4-87cc-785399803b4b.png)
![1](https://user-images.githubusercontent.com/68970106/223751725-19cfc9c4-a8b1-48f4-b846-3491dad4d616.png)
![2](https://user-images.githubusercontent.com/68970106/223751726-825bc25b-4922-40ce-80dd-c6c552357552.png)
![3](https://user-images.githubusercontent.com/68970106/223751728-98b44855-de2b-4c82-912c-73f820ac4210.png)
![4](https://user-images.githubusercontent.com/68970106/223751732-f050ef68-dba5-4d2a-8b41-6db1a23254dd.png)
![5](https://user-images.githubusercontent.com/68970106/223751736-917ccdfb-334b-4724-81ab-fda3801905aa.png)
![6](https://user-images.githubusercontent.com/68970106/223751738-21ce41fc-bb52-4e4e-8985-cfc8597de507.png)

# 2. Configuración de certificados en el servidor.

## 2.1- Creamos la carpeta ssl en el proyecto.
```
sudo mkdir ~/pypractice/.config/ssl_certs
```

## 2.2- Creamos los certificados
```
sudo touch ~/pypractice/.config/ssl_certs/djangobase.net.crt
sudo touch ~/pypractice/.config/ssl_certs/djangobase.net.key
```

## 2.3- Copiar y pegar el contenido .crt que nos genero cloudflare.
```
sudo nano ~/pypractice/.config/ssl_certs/djangobase.net.crt
```

## 2.4- Copiar y pegar el contenido .key que nos genero cloudflare.
```
sudo nano ~/pypractice/.config/ssl_certs/djangobase.net.key;
```

## 2.4 Editamos el nginx de nuestro proyecto.

    sudo nano /etc/nginx/sites-available/pypractice

Y en las rutas __ssl_certificate__ __ssl_certificate_key__ agregamos lo siguiente. Ejemplo.

    ssl_certificate       /home/pypractice_server/pypractice/.config/ssl_certs/djangobase.net.crt;
    ssl_certificate_key   /home/pypractice_server/pypractice/.config/ssl_certs/djangobase.net.key;


## 2.5. Probamos que el SSL del servidor sea valido aqui: https://www.digicert.com/help/
Debemos marcar la casilla **Check for common vulnerabilities**

Probamos con:

- djangobase.net
- www.djangobase.net

Todas deben funcionar correctamente.
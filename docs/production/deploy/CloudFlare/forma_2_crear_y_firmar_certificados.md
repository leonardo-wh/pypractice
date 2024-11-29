### 16. Generar certificados SSL

__16.1__ Generamos archivo .csr para que rapidssl nos firme el certificado para ello ejecutamos el siguiente comando:

    openssl req -nodes -newkey rsa:2048 -keyout ~/pypractice/.config/ssl_certs/2023/djangobase.net.key -out ~/pypractice/.config/ssl_certs/2023/djangobase.net.csr

El archivo *djangobase.net.key* se utiliza para generar el archivo **djangobase.net.csr** el cual se utiliza para que se generen los certificados.


__16.2__ El ejecutar el comando anterior solicitara los datos del CSR

    Country Name (2 letter code) [AU]:MX
    State or Province Name (full name) [Some-State]:MX
    Locality Name (eg, city) []:MX
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:DjangoBase
    Organizational Unit Name (eg, section) []:DjangoBase
    Common Name (e.g. server FQDN or YOUR name) []:*.djangobase.net
    Email Address []:ventas@alomvpn.com
    Please enter the following 'extra' attributes
    to be sent with your certificate request
    A challenge password []:xkpj3cuentas
    An optional company name []:DjangoBase

__16.3__ Despues de llenar los datos, el archivo (o el contenid) podrá subirse en name.com para que se genere la firma de SSL. 

Una vez se tenga la firma, se crea un archivo llamado ssl.crt dentro de la carpeta del año correspondiente. Ejemplo

    nano ~/pypractice/.config/ssl_certs/2023/ssl.crt

En ese archivo colocamos el contenido de la firma que nos deviolvio Comodo/RapidSSL. Una vez se tenga la firma, procederemos a realizar lo siguiente:

Concatenamos crt que nos dio name + intermediate y lo subimos al server:

    cat ssl.crt intermediate.crt >> djangobase.net.crt

**Nota:** El archivo intermediate se encuentra en **/home/pypractice_server/pypractice/.config/ssl_certs/2023/**

__16.4__ Editamos el nginx de nuestro proyecto.

    sudo nano /etc/nginx/sites-available/pypractice

Y en las rutas __ssl_certificate__ __ssl_certificate_key__ agregamos lo siguiente. Ejemplo.

    ssl_certificate       /home/pypractice_server/pypractice/.config/ssl_certs/djangobase.net.crt;
    ssl_certificate_key   /home/pypractice_server/pypractice/.config/ssl_certs/djangobase.net.key;


__16.5__ Probamos que el SSL del servidor sea valido aqui: https://www.digicert.com/help/
Debemos marcar la casilla **Check for common vulnerabilities**

Probamos con:

- djangobase.net
- www.djangobase.net

Todas deben funcionar correctamente.
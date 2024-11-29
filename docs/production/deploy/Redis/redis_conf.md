# Ligar diferentes servidores al mismo servidor de Redis (Binding)

> Informacion obtenida de: https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04

## Instalar redis

    sudo apt update
    sudo apt install redis-server

__1.-__ Cambiamos el archivo de redis
    
    sudo nano /etc/redis/redis.conf

__2.-__ Buscamos con ctrl+w la linea que concuerde con "bind 127". Agregamos la ip del servidor

    # bind 127.0.0.1 IP_privada_server ejemplo: 
    bind 127.0.0.1 172.31.227.208

__3.-__ Si se desea asignar una contraseña, en una terminal aparte hacemos lo siguiente
    
    echo "tucontraseña" | sha1sum
    
    XXSWDb4FDSbFDdcSDS4dDS3Se44234a53e7e2e025dc5bde4XD12
    
__4.-__ En el archivo de redis.conf buscamos "requirepass", estara comentada. Cambiamos lo que tenia por la contraseña que se creo con anterioridad

    requirepass XXSWDb4FDSbFDdcSDS4dDS3Se44234a53e7e2e025dc5bde4XD12

__5.-__ Cerramos el documento y reiniciamos el servicio
    
    sudo service redis-server restart


__6.-__ Editar nuestras variables de productos .env de nuestro proyeto.

    sudo nano hunabku/.config/environment/production/.env
    
-Buscar las siguientes variables (Si no las tiene, agregarlas).
    
    REDIS_SERVER=redis://:<mipassword_redis>@<ip_privada_server>:6379/1
    CELERY_BROKER_URL=redis://:<mipassword_redis>@<ip_privada_server>:6379/
    REDIS_DJANGO_WS_CHANNELS=redis://:<mipassword_redis>@<ip_privada_server>:6379/0
    
Ejemplo:

    REDIS_SERVER=redis://:XXSWDb4FDSbFDdcSDS4dDS3Se44234a53e7e2e025dc5bde4XD12@172.31.227.208:6379/1
    CELERY_BROKER_URL=redis://:XXSWDb4FDSbFDdcSDS4dDS3Se44234a53e7e2e025dc5bde4XD12@172.31.227.208:6379/
    REDIS_DJANGO_WS_CHANNELS=redis://:XXSWDb4FDSbFDdcSDS4dDS3Se44234a53e7e2e025dc5bde4XD12@172.20.1.89:6379/0
    
__7.-__ Modificar nuestro archivo settings.py

    sudo nano /etc/supervisor/conf.d/hunabku.conf

**Nota:** Verificar en el siguiente archivo si contamos con la variable **REDIS_DJANGO_WS_CHANNELS**

__7.1__ buscar la seccion **env = environ.Env(** y debe de estar de la siguiente manera (en caso de no estar agregarla)

    REDIS_DJANGO_WS_CHANNELS=str,

__7.2__ buscar la seccion **CHANNEL_LAYERS** y verificar la variable se encuetre de la siguiente manera: **REDIS_DJANGO_WS_CHANNELS**

```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_DJANGO_WS_CHANNELS)],
        },
    },
}
```


__8__ Reinicia redis.

    sudo systemctl restart redis

__9__ En otra terminal redis

    redis-cli

Una vez estando dentro del cli de redis, nos autenticamos con nuestra password.

    127.0.0.1:6379> auth su_password_redis
    OK

Ejecutamos el comando PING.

    127.0.0.1:6379> PING

Deberias ver la siguiente salida, si es asi, todo esta correcto.

    Output:
    PONG
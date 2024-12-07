# PyPractice


Si es primera vez ejecutar:
```
CONDITION=CREATE docker-compose up --build
```

Si no:
```
docker-compose up
```

Si se desea entrar en la consola y crear un superusuario ejecutar 
```
docker-compose exec web bash
```

Entrar en el entorno con:
```
pipenv shell
```

Crear superuser:
```
python manage.py createsuperuser
```

....etc
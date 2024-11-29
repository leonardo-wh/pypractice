Es posible comenzar a modularizar el proyecto, en especial cuando:

1. los modelos empiezan a crecer en atributos o métodos, y
2. cuando las views comienzar a tener mucha lógica. Esto incrementa el número de lineas en el archivo y lo hace complicado de leer.

- Ejemplo de app sin modularizar

  ```
  └── apps/
     └── users/
         ├── __init__.py
         ├── migrations/
         ├── admin.py
         ├── apps.py
         ├── models.py
         ├── tests.py
         └── views.py
  ```

- Ejemplo de app modularizada

  ```
  └── apps/
   └── sistema/
       ├── __init__.py
       ├── migrations/
       ├── admin.py
       ├── apps.py
       ├── tests.py
       ├── models.py
       ├── utils.py
       ├── templatetags/
       ├── templates/
       │   └── plan_internet/
       │      └── archivos.html
       ├── cache/
       │	 ├── __init__.py
       │   └── plan_internet_cache.py
       ├── tasks/
       │	 ├── __init__.py
       │   └── plan_internet_tasks.py
       ├── forms/
       │	 ├── __init__.py
       │   └── plan_internet_forms.py
       └── views/
           ├── __init__.py
           ├── plan_internet_views.py
           ├── ...
           └── router_views.py
  ```

Antes de pensar en modularizar como el ejemplo anterior hay que tener encuenta que realizar el import cuesta espacio en memoria. Por lo que consume menos memoria tener todos los modelos en un archivo que tener modelos o vistas divididos por archivos.

El modularizar dependera si la aplicación es altamente consumida (por ejemplo facturas en WispHub). En ese escenario debemos darle prioridad al performance que en la legibilidad. Pero si es una app que no es muy consumida pero sus modelos o vistas son extensos podemos dar prioridad a la legibilidad y modularizar

Una alternativa intermedia es mantener la siguiente estructura. Donde se modulariza unicamente el modelo mas extenso **Facturas** situandolo en el archivo `models/facturas.py` y todos los demas modelos se encuentran en `models/commons.py`

```
└── apps/
   └── wisp_facturas/
       ├── __init__.py
       ├── migrations/
       ├── admin.py
       ├── apps.py
       ├── tests.py
       ├── models/
       │   ├── __init__.py
       │   ├── commons.py
       │   └── facturas.py
       └── views.py
```

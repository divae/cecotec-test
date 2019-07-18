
Prueba técnica Cecotec: Estela Medrano | 
Django - Docker
====================

### Pre requisito

* Tener instalado **Docker** y **Docker-compose**. Si está utilizando Mac OS X instale **Docker Toolbox**.

## Repositorio del projecto.

**_Descargar estructura del proyecto de GitHub_**

Se descarga el proyecto que contiene la estructura general.

```bash
$ git clone https://github.com/divae/cecotec-test.git
```

## Generar la imagen de Docker del proyecto.

**_Imagen en Docker_**

El fichero `requirements.txt` contiene las dependencias del proyecto, para este caso he usado:

- Django>=2.1.3,<2.2.0
- djangorestframework>=3.9.0,<3.10.0
- flake8>=3.6.0,<3.7.0

```bash
$ docker-compose build
```


## Si es la primera vez que se arranca el proyecto

- Generar las migraciones migrations
```bash
$ docker-compose run app sh -c "python manage.py migrate"
```
- Generar el super usuario de Django
```bash
$ docker-compose run app sh -c "python manage.py createsuperuser"
```

## Levantar Proyecto Django

```bash
$ docker-compose up
```
**_Probar el sistema_**
Para probar si el sistema acceda a la siguiente dirección [http://localhost:8000](http://localhost:8000). 
El puerto está configurado en el archivo de `docker-compose.yml`.

**_Para el sistema_**
Para detener el sistema en el terminal basta con presionar.
```bash
Ctrl-C
```

**_Para destruir el contenedor_**
```bash
$ docker-compose down
```


## Testear la aplicación

Los test se ejecutan junto a un validadore de estilo de código.
```bash
$ docker-compose run app sh -c "python manage.py test && flake8"
```
## UTILES

**_Usuario creado_**
- email: admin@admin.com
- contraseña: admin
- token: cf3779e814e08d70dd9f04ad8b5271ec1a679d1d

### APIS

- Crear usuario [http://0.0.0.0:8000/api/user/create/](http://0.0.0.0:8000/api/user/create/)
- Crear un token para el usuario [http://0.0.0.0:8000/api/user/token/](http://0.0.0.0:8000/api/user/token/)
- Logearse en la aplicación [http://0.0.0.0:8000/api/user/me/](http://0.0.0.0:8000/api/user/me/)
- Ver productos (necesitas logearte)[http://0.0.0.0:8000/api/product/products/](http://0.0.0.0:8000/api/product/products/)

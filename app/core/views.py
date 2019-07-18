from django.http import HttpResponse

def index(request):

    salute = """Bienvenid@!
    <br>Mi nombre es Estela Medrano (@EstelaYoMisma Twitter) y ha sido un placer realizar ésta prueba,<br> 
    para probar los usuarios recuerda asociar el token a tu navegador mediante extensiones de Chrome 
    como <strong><a href="https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj">'ModHeader'</a></strong>o similares<br><br>
    Para ésta prueba se ha creado: <br>
    usuario: admin@admin.com<br>
    con contraseña: admin <br>
    y token: cf3779e814e08d70dd9f04ad8b5271ec1a679d1d<br><br>
    Puntos de acceso:<br>
    - <a href="http://localhost:8000/api/user/create/">Crear Usuario</a> <br>
    - <a href="http://localhost:8000/api/user/token/">Crear token para el usuario</a> <br>
    - <a href="http://localhost:8000/api/user/me/">Usuario logeado</a> <br><br>

    - <a href="http://localhost:8000/api/product/products/">Productos</a> <br>
    - <a href="http://localhost:8000/api/product/orders/">Carrito</a> <br>
    <br><br>
    ¡Un saludo y espero que la experienia sea agradable!<br><br>
    *** Todos los puntos han sido realizados, el envío de correo faltaría afinarlo ***.
    """
    return HttpResponse(salute)

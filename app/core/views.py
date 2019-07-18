from django.http import HttpResponse

def index(request):
    return HttpResponse("Bienvenid@!<br>Mi nombre es Estela Medrano (@EstelaYoMisma Twitter) y ha sido un placer realizar ésta prueba, para probar los usuarios recuerda asociar el token a tu navegador mediante extensiones de Chrome como <strong>'ModHeader'</strong> o similares<br><br>Para esta prueba se ha creado: <br>usuario: admin@admin.com<br>con contraseña: admin <br>y token: cf3779e814e08d70dd9f04ad8b5271ec1a679d1d<br><br>¡Un saludo y espero que la experienia sea agradable!")



# Primero, importamos los serializadores
from apps.e_commerce.api.serializers import *

# Segundo, importamos los modelos:
from django.contrib.auth.models import User
from apps.e_commerce.models import Comic,WishList

# Luego importamos las herramientas para crear las api views con Django REST FRAMEWORK:

# # (GET) Listar todos los elementos en la entidad:
# from rest_framework.generics import ListAPIView

# # (POST) Inserta elementos en la DB
# from rest_framework.generics import CreateAPIView

# # (GET-POST) Para ver e insertar elementos en la DB
# from rest_framework.generics import ListCreateAPIView

# from rest_framework.generics import RetrieveUpdateAPIView

# from rest_framework.generics import DestroyAPIView

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView
)

# Importamos librerías para gestionar los permisos de acceso a nuestras APIs
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


mensaje_headder = '''
Ejemplo de header:

`headers = {
  'Authorization': 'Token 92937874f377a1ea17f7637ee07208622e5cb5e6',
  'actions': 'PUT',
  'Content-Type': 'application/json',
  'Cookie': 'csrftoken=cfEuCX6qThpN6UC9eXypC71j6A4KJQagRSojPnqXfZjN5wJg09hXXQKCU8VflLDR'
}`
'''
# NOTE: APIs genéricas:

class GetComicAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]



class PostComicAPIView(CreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-POST]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    Tambien nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro, o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DestroyComicAPIView(DestroyAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO DELETE]`
    Esta vista de API nos permite eliminar un registro de la Base de Datos.
    Debemos pasarle un argumento estático en la url <pk>.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# NOTE: APIs MIXTAS:

class GetOneComicAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve un comic en particular de la base de datos.
    '''
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        '''
        Sobrescribimos la función `get_queryset` para poder filtrar el request 
        por medio de la url. En este caso traemos de la url por medio de `self.kwargs` 
        el parámetro `comic_id` y con él realizamos una query para traer 
        el comic del ID solicitado.  
        '''
        try:
            comic_id = self.kwargs['comic_id']
            queryset = Comic.objects.filter(id=comic_id)
            return queryset
        except Exception as error:
            return {'error': f'Ha ocurrido la siguiente excepción: {error}'}

class LoginUserAPIView(APIView):
    '''
    Vista de API personalizada para recibir peticiones de tipo POST.
    Esquema de entrada:
    {"username":"root", "password":12345}
    
    Utilizaremos JSONParser para tener  'Content-Type': 'application/json'
    '''
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = []

    def post(self, request,format=None):
        '''
        Esta función sobrescribe la función post original de esta clase,
        recibe "request" y hay que setear format=None, para poder recibir los datos en request.data 
        la idea es obtener los datos enviados en el request y autenticar al usuario con la 
        función "authenticate()", la cual devuelve el estado de autenticación.
        \nLuego con estos datos se consulta el Token generado para el usuario, si no lo tiene asignado,
        se crea automáticamente.
        \nEsquema de entrada:
        \n`{"username":"root", "password":12345}`
        \nUtilizaremos JSONParser para tener  `'Content-Type': 'application/json'`
        '''
        user_data = {}
        try:
            # Obtenemos los datos del request:
            username = request.data.get('username')
            password = request.data.get('password')
            # Obtenemos el objeto del modelo user, a partir del usuario y contraseña,
            # NOTE: es importante el uso de este método, porque aplica el hash del password!
            account = authenticate(username=username, password=password)

            if account:
                # Si el usuario existe y sus credenciales son validas, tratamos de obtener el TOKEN:
                try:
                    token = Token.objects.get(user=account)
                except Token.DoesNotExist:
                    # Si el TOKEN del usuario no existe, lo creamos automáticamente:
                    token = Token.objects.create(user=account)
                # Con todos estos datos, construimos un JSON de respuesta:
                user_data['user_id'] = account.pk
                user_data['username'] = username
                user_data['first_name'] = account.first_name
                user_data['last_name'] = account.first_name
                user_data['email']=account.email
                user_data['is_active'] = account.is_active
                user_data['token'] = token.key                
                # Devolvemos la respuesta personalizada
                return Response(user_data)
            else:
                # Si las credenciales son invalidas, devolvemos algun mensaje de error:
                user_data['response'] = 'Error'
                user_data['error_message'] = 'Credenciales invalidas'
                return Response(user_data)

        except Exception as error:
            # Si aparece alguna excepción, devolvemos un mensaje de error
            user_data['response'] = 'Error'
            user_data['error_message'] = error
            return Response(user_data)

# TODO: Agregar las vistas genericas que permitan realizar un CRUD del modelo de wish-list.
# TODO: Crear una vista generica modificada para traer todos los comics que tiene un usuario.

class GetWishListAPIView(ListAPIView):
    __doc__ = f'''
    [MÉTODO GET]
    Esta vista de API nos devuelve una lista de las WishList
    de aquellos usuarios presentes en la Base de Datos.

    - Ejemplo de url:
        http://localhost:8000/e-commerce/wishlist/get
    '''

    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class PostWishListAPIView(CreateAPIView):
    __doc__ = f'''
    [MÉTODO POST]
    Esta Vista de API nos permite realizar un 'insert'
    en la Base Datos.

    - Ejemplo de url:
        http://localhost:8000/e-commerce/wishlist/post
    '''

    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class ListCreateWishListAPIView(ListCreateAPIView):
    __doc__ = f'''
    [MÉTODO GET/POST]
    Esta Vista de API nos permite visualizar todos los usuarios 
    con sus WishList y a su vez, si se desea poder realizar un 
    'insert' en la Base Datos.

    - Ejemplo de url:
        http://localhost:8000/e-commerce/wishlist/get-post
    '''
    queryset =  WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class RetrieveUpdateListWishAPIView(RetrieveUpdateAPIView):
    __doc__ = '''
    [MÉTODO GET-PUT-PATCH]
    Esta vista de API nos permite actualizar un sólo registro, o simplemente visualizarlo.
    Debemos pasarle un argumento estático en la url <pk>.

    - Ejemplo de url:
        http://localhost:8000/e-commerce/wishlist/<id>/update

    - El parámetro 'id' o 'pk' es el nro. de indentificación del usuario.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class DestroyWishListAPIView(DestroyAPIView):
    __doc__ = '''
    [MÉTODO DELETE]
    Esta vista de API nos permite eliminar un registro de la Base de Datos.
    Debemos pasarle un argumento estático en la url <pk>.
    
    - Ejemplo de url:
        http://localhost:8000/e-commerce/wishlist/<id>/delete

    - El parámetro 'id' o 'pk' es el nro. de indentificación del usuario.
    '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


# NOTE: API-MIXTA O API GENÉRICA-PERSONALIZADA:

class GetUserFavsAPIView(ListAPIView):
    __doc__ = '''
    [MÉTODO GET]
    Esta Vista de API nos devuelve los comics 
    favoritos de un usuario particular, que será
    filtrado, en este caso, debemos pasarle un 
    argumento estático en la url el <username>.

    - Ejemplo de url:
        http://localhost:8000/e-commerce/wishlist/<username>/get
    '''
    serializer_class = ComicSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def get_queryset(self):
        '''
        Sobrescribimos la función `get_queryset` para poder filtrar el request 
        por medio de la url. En este caso traemos de la url por medio de `self.kwargs` 
        el parámetro `username` y con él realizamos una query para traer 
        los comics favoritos del "usuario" solicitado.  
        '''
        try:
            comic_ids = []

            user_name = self.kwargs['username']
            user = User.objects.filter(username=user_name)  # Obtengo una queryset del modelo User filtrando por el username.
            user_id = user[0].pk    # user_id = user.first().id    # Obtengo el user_id correspondiente al username.
            
            # Realizo una nueva queryset ahora del modelo WishList filtrando
            # por el user_id y si tiene favoritos.
            wish_list= WishList.objects.filter(user_id=user_id, favorite=True)
            
            # Recorro los queryset devueltos y obtengo el comic_id de c/u para luego
            # almacenarlo en una lista y pasarsela a una nueva queryset que me devuelve
            # los comics.
            for i in wish_list.values_list('comic_id'):
                comic_ids.append(i[0])
            comic_obj = Comic.objects.filter(id__in=comic_ids)  # Utilizo id__in que le asigna un iterador
            return comic_obj

        except Exception as error:
            return {'error': f'ha ocurrido la siguiente expeción: {error}'}


class PostUserFavsAPIView(APIView):
    __doc__ = '''
    Vista de API personalizada para recibir peticiones de tipo POST.
    
    - Esquema de entrada:
        {"username":"root"}
    
    Esta Vista de API nos devuelve los comics 
    favoritos de un usuario particular, que será
                filtrado, en este caso, por el 'username'.
    '''

    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        '''
            Función post sobreescribida verifica que el 'username'
            pasado exista, de ser así devuelve, la lista de comics
            favoritos del mismo.\n 
            Se debe pasar en el body del mensaje
            HTTP un esquema de entrada.

            - Content-Type': 'application/json'
            - Esquema de entrada:
                {"username":"root", "password":12345}
        '''
        comic_data = {}
        user_data = []
        try:
            user_name = request.data.get('username')
            user = User.objects.filter(username=user_name)

            if user:  # Pregunto si existe la cuenta con dicho username
                wish_list = WishList.objects.filter(user_id=user.first().pk, favorite=True)
                for comic in wish_list.values('comic_id'):
                    id = comic['comic_id']
                    comic_obj = Comic.objects.filter(id=id).first()

                    comic_data['marvel_id'] = comic_obj.marvel_id
                    comic_data['title'] = comic_obj.title
                    comic_data['description'] = comic_obj.description
                    comic_data['price'] = comic_obj.price
                    comic_data['stock_qty'] = comic_obj.stock_qty
                    comic_data['picture'] = comic_obj.picture

                    user_data.append(comic_data)

                return Response(user_data)
            
            else:
                return Response({'username': 'does not exist'})

        except Exception as error:
            return Response({'error': f'hola'})
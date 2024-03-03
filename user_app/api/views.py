from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer, SerializerRegistroJWT
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken 



@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete() 
        return Response(status=status.HTTP_200_OK)
@api_view(['POST'])
def Registrate_a(request):
    de_serializer = RegistrationSerializer(data=request.data)
    data = {}  
    if de_serializer.is_valid():
        account = de_serializer.save()  
        data['response'] = 'La respuesta fue obtenida exitosamente'
        data['username'] = account.username
        data['email'] = account.email
        #todo: para obtener el token creado con el signals post_save
        token = Token.objects.get(user=account).key
        data['token'] = token        
        print("la cuenta es:")
        print(account)
        return Response(data)

@api_view(['POST'])
def Registrate_now(request):
    if request.method == 'POST': 
        de_serializer = RegistrationSerializer(data= request.data) 
        data = {}
        if de_serializer.is_valid(): 
            account =  de_serializer.save() 
            data['response'] = 'Tuvo exito'
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['apellido'] = account.apellido
            data['phone_number'] = account.phone_number
            refresh = RefreshToken.for_user(account) 
            data['token'] = {
                'refresh':str(refresh), 
                'access': str(refresh.access_token)
            }
            return Response(data)

from user_app.models import Account
from django.contrib import auth
@api_view(['POST'])
def login_view1(request):
    data = {}
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        account = auth.authenticate(email=email, password=password)

        if account is not None: 
            data['response'] = 'El login fue exitosopasd'
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.apellido
            data['phone_number'] = account.phone_number
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh':str(refresh), 
                    'access': str(refresh.access_token)
                }
            return Response(data)
        else:
            data['error'] = 'Credenciales incorrectas'
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




 



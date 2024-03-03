from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import *


#todo: carpeta 9 Json Web Token(JWT)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #path('login/', obtain_auth_token, name='login'), #Logeo usando TokenAuthentication
    #*LOGEO PERSONALIZADO
    path('login-app/', login_view1, name='login-app'),
    path('logout/', logout_view, name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/register/', Registrate_now, name='token_register')

]



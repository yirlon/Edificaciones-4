from inmuebleslist_app.models import Inmuebles, Empresa, Comment #Customer
from rest_framework.response import Response
from inmuebleslist_app.api.serializers import InmueblesSerializer, EmpresaSerializer, CommentarioSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from inmuebleslist_app.api.permissions import IsAdminOrReadOnly, IsComentarioUserReadOnly, IsCommentReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle   
from inmuebleslist_app.api.throttling import ComentarioCreateThrottling, ComentarioListThrottling
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


class Inmuebles_list(APIView):
    permission_classes =[IsAdminOrReadOnly]  
    def get(self, request):
        inmuebles = Inmuebles.objects.all()
        serializer = InmueblesSerializer(inmuebles, many=True, context={'request':request})
        return Response( serializer.data)
    def post(self, request):
        deserializer = InmueblesSerializer(data=request.data)
        if deserializer.is_valid():
            deserializer.save()
            return Response( deserializer.data)
        else:
            return Response( deserializer.errors, status=status.HTTP_400_BAD_REQUEST)

class inmueble_detalle(APIView):
    #*Ver inmueble correspondiente
    def get(self, request, pk):
        try:
            inmueble = Inmuebles.objects.get(pk=pk)
            serializer = InmueblesSerializer( inmueble, context= {'request':request} )
            return Response( serializer.data)
        except Inmuebles.DoesNotExist:
            mensaje = {"mensaje":"el record no existe"}
            return Response(mensaje["mensaje"], status=status.HTTP_404_NOT_FOUND)
        #*actualizar inmueble
    def put(self, request, pk):
        inmueble = Inmuebles.objects.get(pk=pk)
        de_serializer = InmueblesSerializer(inmueble, data=request.data)
        if de_serializer.is_valid():
            de_serializer.save()
            return Response(de_serializer.data)
        else:
            return Response(de_serializer.errors)
    #*borrar inmueble
    def delete(self, request, pk):
        try:
            inmueble = Inmuebles.objects.get(pk=pk)
            inmueble.delete()
        except:
            return Response({"mensaje":"no hay nada q elimina pq no existe"}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
class EmpresaAV(APIView):
    #*consulta de las empresas
    def get(self, request):
        empresa = Empresa.objects.all()
        serializer = EmpresaSerializer(empresa, many=True, context = {'request':request})
      
        return Response( serializer.data )
    #*agregar una nueva empresa
    def post(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmpresaDetalleAV(APIView):

    def get(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)    
        except Empresa.DoesNotExist:
            return Response({"mensaje":"la empresa no existe"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmpresaSerializer(empresa, context = {'request':request})
        return Response(serializer.data)
        
    #*actualizar empresa
    def put(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)                       
            de_serializer = EmpresaSerializer(empresa, data=request.data, context= {'request':request}) 
            if de_serializer.is_valid():
                de_serializer.save() 
                return Response( de_serializer.data)
            else:
                return Response( de_serializer.errors)
        except Empresa.DoesNotExist:
            return Response({"mensaje":"empresa no encontrada"}, status=status.HTTP_401_UNAUTHORIZED)

    #*borrar empresa
    def delete(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk) #aqui busco el registro para eliminar
            empresa.delete()
        except Empresa.DoesNotExist:
            mensaje = {"mensaje":"No se puede eliminar una empresa q no existe"}
            return Response(mensaje["mensaje"], status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class Comentarioslist(APIView):
    def get(self, request):
        try:
            comentarios = Comment.objects.all()
            serializer = CommentarioSerializer(comentarios,many=True, context = {'request':request})
            return Response(serializer.data)
        except Comment.DoesNotExist:
            return Response({"mensaje":"Comentario no existe"}, status=status.HTTP_404_NOT_FOUND)

    
class Inmuebles_detalles(APIView):
    def get(self, request, pk):
        customer = request.user.customer
        print(customer)
        try:
            inmueble = Inmuebles.objects.get(pk=pk)
            comentario = Comment.objects.filter(inmueble=inmueble)
            serializer = CommentarioSerializer(comentario, many=True)
            print(type(serializer))
            print(serializer)
        except:
            mensaje = {"mensaje":"la data no fue encontrada"}
            return Response(mensaje["mensaje"], status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)
 

class ComentarioCreate(generics.CreateAPIView):#todo: solo permite el post 
    serializer_class = CommentarioSerializer
    def perform_create(self, serializer): 
        pk = self.kwargs.get('pk')
        inmuebles =  Inmuebles.objects.get(pk=pk)
        user = self.request.user #todo: para ver el usuario actual registrado 
        comentario_queryset = Comment.objects.filter(inmueble=inmuebles, comentario_user=user)    
        if comentario_queryset.exists(): 
            raise ValidationError("el usuario ya escribio un comentario para este inmueble") 
        
        if inmuebles.number_calificacion == 0:
            inmuebles.avg_calificacion = serializer.validated_data['calificacion']
        else:      
            inmuebles.avg_calificacion = (serializer.validated_data['calificacion'] + inmuebles.avg_calificacion)/2
        inmuebles.number_calificacion = inmuebles.number_calificacion + 1 
        inmuebles.save() 

        serializer.save(inmueble=inmuebles, comentario_user=user)

    def get_queryset(self):
        return Comment.objects.all()

        
  
class ComentariosList(generics.ListCreateAPIView): #todo:ListCreateAPIView permite get y post 
    throttle_classes = [ComentarioListThrottling, AnonRateThrottle]
    serializer_class = CommentarioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comentario_user__username', 'active'] 
   
    def get_queryset(self): 
        pk = self.kwargs['pk']    
        return Comment.objects.filter(inmueble=pk) 

class ComentarioDetaill(generics.RetrieveUpdateAPIView):
    permission_classes = [IsCommentReadOnly]
    serializer_class = CommentarioSerializer
    queryset = Comment.objects.all()
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comentario-detail' 
    

class EmpresaVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly] #!Permiso personalizado
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer



class UsuarioComentario(generics.ListAPIView):
    serializer_class = CommentarioSerializer
    def get_queryset(self):
        username = self.request.query_params.get('usernamee', None)
        return Comment.objects.filter(comentario_user__username = username) 
   
      
 

from inmuebleslist_app.api.pagination import InmueblesPagination, InmueblesLOPagination

class EdificacionList(generics.ListAPIView):
    queryset = Inmuebles.objects.all()
    serializer_class = InmueblesSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['direccion', 'empresa__nombre', 'pais']
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'edificacion-list'
    pagination_class = InmueblesLOPagination 













    
    































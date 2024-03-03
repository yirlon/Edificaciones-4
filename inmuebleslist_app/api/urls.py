from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inmuebleslist_app.api.views import * 

router = DefaultRouter()
router.register('empresa', EmpresaVS, basename='empresa')


urlpatterns = [
    path('edificacion/', Inmuebles_list.as_view(), name="inmuebles-detail"),
    path('edificacion/<int:pk>', inmueble_detalle.as_view() , name="inmuebles-detail"),
    path('', include(router.urls)),
    path('empresa/', EmpresaAV.as_view() , name="empresa"),
    path('empresa/<int:pk>', EmpresaDetalleAV.as_view() , name="empresa-detail"),
    path('<int:pk>/comments', Inmuebles_detalles.as_view() , name="comments"),
    path("edificacion/<int:pk>/comentario-create", ComentarioCreate.as_view(), name="comentarios-create"),
    path("edificacion/<int:pk>/comentario/", ComentariosList.as_view(), name="comentarios-list"),
    path("edificacion/comentario/<int:pk>/", ComentarioDetaill.as_view(), name="comentarios-detail"),
    path("edificacion/comentario/", UsuarioComentario.as_view(), name="usuario-comentarios-detail"),
    path('edificacion/list/', EdificacionList.as_view(), name='edificacion-list')
]

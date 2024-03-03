from rest_framework import serializers
from inmuebleslist_app.models import Inmuebles, Empresa, Comment




class CommentarioSerializer(serializers.ModelSerializer):
   
    comentario_user = serializers.StringRelatedField(read_only=True) 
    class Meta:
        model = Comment
       
        exclude = ['inmueble'] 


class InmueblesSerializer(serializers.ModelSerializer):
   
    comments = CommentarioSerializer(many=True, read_only=True) 
    
    empresa = serializers.CharField(source='empresa.nombre')
    class Meta:
        model = Inmuebles 
        fields = "__all__"
      

class EmpresaSerializer(serializers.ModelSerializer):
    edificacionlist = InmueblesSerializer(many=True, read_only=True) 
    
    class Meta:
        model = Empresa
        fields = "__all__"










       








        

    






    
    
   
        





    




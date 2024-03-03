from rest_framework import serializers
from django.contrib.auth.models import User



from user_app.models import Account   
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:  
        model = Account 
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'apellido', 'phone_number']
        extra_kwargs = {
            'password': {'write_only':True}
        } 
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"error":"El password de confirmación no coincide"})
        if Account.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'El email del usuario ya existe'})
        account = Account.objects.create(first_name =self.validated_data['first_name'], 
                                         apellido=self.validated_data['apellido'],
                                         email= self.validated_data['email'],
                                         username = self.validated_data['username'],
                                         password = self.validated_data['password']  
                                         )
        account.set_password(password) 
        account.phone_number= self.validated_data['phone_number']
        account.save()                 
        return account  
    
class SerializerRegistroJWT(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User  
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}

        }
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
  
        if password != password2:
            raise serializers.ValidationError("Los campos no coinciden")

        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError("el email ya existe, escriba otro")
        
        account =   User(email = self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account 
    

        
        

        
        
        
        


      

































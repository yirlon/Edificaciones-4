from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    #*creacion de usuario normal
    def create_user(self, first_name, apellido, username, email, phone_number, password=None):
        if not email:
            raise ValueError('El usuario no tiene email')
        if not username:
            raise ValueError('El usuario no tiene username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name= first_name,
            apellido = apellido,
            phone_number = phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, apellido, username, email, phone_number, password):
        user = self.create_user(
            email = self.normalize_email(email), 
            username = username, 
            password = password,
            first_name= first_name,
            apellido= apellido,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)
    date_joinet = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
   
    REQUIRED_FIELDS = ['username', 'first_name', 'apellido', 'phone_number']  

    objects = MyAccountManager() 
    def full_name(self):
        return f'{self.first_name} {self.apellido}'
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, add_label):
        return True
    












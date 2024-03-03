from django.contrib import admin

# Register your models here.

from inmuebleslist_app.models import Inmuebles, Empresa, Comment #Customer






admin.site.register( Comment )
admin.site.register( Inmuebles )
admin.site.register( Empresa )


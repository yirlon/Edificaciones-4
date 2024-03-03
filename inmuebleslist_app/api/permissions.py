
#todo: esto es de la carpeta 7 creando permisos perzonalizados: osea en vez de heredar de IsAuthenticated, pues darle un permiso
#todo: personalizado con la idea de q se pueda acceder a la lectura de Empresa( consulta ) sin estar autheticado pero q para 
#todo: realizar una edicion( put ) o creación( post ) halla q estar authenticado en el sistema.
from rest_framework import permissions
from inmuebleslist_app.models import Comment

from rest_framework.validators import ValidationError 

#*CREACION DE MIS PROPIOS PERMISOS PERSONALIZADOS
class IsAdminOrReadOnly(permissions.IsAdminUser):
#todo: DETALLE SUPER IMPORTANTE: from rest_framework.permissions import IsAdminUser si hubiera echo esto seria lo mismo poner q mi
#todo:clase herede de IsAdminUser

#!voy a sobreescribir este método, esto quiere decir q a la clase Isadmin le estoy sobreescribiendo el metodo has_permission q le 
#!viene por defecto, es aqui la personalizacion de mi permiso.
    #!has significa tiene osea: tiene permiso
    def has_permission(self, request, view):#*esta función o método es heredada del IsAdminUser y va a tener stos 3 parametro x default
        #todo: el view será la vista a la q estará asiganada esta clase AdminOrReadOnly
    #!el usuaro puede leer la data bajo el método get y por eso se le pone aqui q si se hace un get pues q diga q true y q se pueda
        print("El view es")
        print( view )
        if request.method == 'GET': 
            return True;    #!cuando lee este return pues aqui mismo se corta e ignora lo de abajo
            #*obtengo el tipo de permiso q tengo dependiedo de la sesion del usuario
            #todo: con request.user y request.user.is_staff se estan evaluando dos condiciones q son si el usuario es registrado y si es
            #todo: ademas es staff osea q sino es staff pues tampoco podrá accede, ojo: request.user y request.user.is_autheticated es
            #todo: practicamente lo mismo ya q request.user significa si existe el usuario y devolverña q True y request.user.is_athe..
            #todo: significa q si el usuario esta autenticado y dirá q True en caso q lo este y False en caso q no lo este
        staff_permission = bool(request.user.is_authenticated and request.user.is_staff)#!sino entra en el if de arriba pues entra aquí ya q es un post o
                                                                        #!o put y entonces mira si es staff y si lo es pues devuelve True
                                                                        #! y sino lo es pues devuelve false y no puede acceder al post
        return staff_permission   
        #!hago esto con bool pq este método de has_permission tiene q devolver un booleano ya sea True o False
    
#*************************************FORMA MÍA DE HACERLO**************************************************************************
class IsComentarioUserReadOnly(permissions.IsAdminUser):#la clase adminUser es del administrador(panel de control) de permisos de usuario
    def has_permission(self, request, view):
        # print("el valor del request es")
        # print(request) #<rest_framework.request.Request: OPTIONS '/tienda/edificacion/2/comentario'>
        if request.method == 'GET': 
            print("metodo get")
            return True
        #TODO: PQ NO ME SALIA EL POST EN LA CONSULTA SI TODO ESTABA BIEN: NO ME SALIA PQ TENIA Q HACER UNA DEVOLUCION DE UN VALOR
        #TODO: PARA Q LE DIJERA Q TIENE Q HACER EN CASO Q FUERA POST Y PARA Q SALIERA PUES HABIA Q DEVOLVER ALGO, OJO: AQUI SI HAGO ESTO
        #TODO:  if request.method == 'PUT': Y NO HAGO EL DEL POST PES EL POST NO ME SALE HASTA Q NO LO HAGA, Y EL PUT ME SALDRÁ PERO
        #TODO: EN LA CUANDO LE PONGA UN ID EN LA URL OSEA DJANGO LO ENTRERÁ Y SALDRA SIMPRE Y CUANDO AQUI LO CUBRA CON UN VALOR, 
        #TODO: OJOOO NO ERA PQ listCreateApiView FUNCINABA DIFERENTE A ModelViewSet
        
        if request.method == 'PUT': #TODO: OJO: ESTA LINEA ES COMO SI NO EXISTIERA PQ NO VA A ESPERAR PQ SE HAGA PUT PARA Q ENTRE AQUI
                                    #TODO: OSEA COMO ESTE METODO YA EXISTE Y LA CLASE RetriveUpdateView igual pues esto va a entender 
                                    #todo: q el put se le muestra en pantalla al cliente en caso de q pase la condicion osea en caso 
                                    #todo: q el cliente logeado es el q creo el comentario pues le da lo opcion para el put y sino pues
                                    #todo: no le da esa opcion
            #print(request.user)
            try:#todo: un try ya q sino le pongo el try pues me sino esta autheticado me da error ya q el request.user no esta disponible
                #!ESTO ES PARA VER SI EL USUARIO CREO EL COMENTARIO:
                comentario_usuario = bool(Comment.objects.filter(comentario_user = request.user))
                #esto filtrando los comentarios del campo comentario_user y viendo si es igual al  usuario actual
                print( comentario_usuario )
                return comentario_usuario
            except:

                #return view #*osea q sino es igual a True osea sino hay usuario pues ejecutame la clase y listame los comentarios
                                #*auqnue asi me devolveria la clase con el put y todo
                return False #!simplemente para q si es false no me salga el metodo put
                #o asi:
                #raise ValidationError("no hay un request.user oea no hay un usuario")
                #Field 'id' expected a number but got <django.contrib.auth.models.AnonymousUser object at 0x0000004F7E491C30>.
                #todo: me daba este error pq
        
#*************************Hecho por el*********************
#*ojo: el lo llama ahora con Basepermission pq parte de la regla del permiso q voy a crear va a necesitar tener acceso a la data actual
#* la cual aplico mi regla
class IsCommentReadOnly(permissions.BasePermission): 

    #todo: El método has_object_permission significa: tiene permiso de objeto
    def has_object_permission(self, request, view, obj): #obj tendrña el valor del modelo q se usa en el serializador en la vista q 
                                                            # va esta clase
        print("valor del view")
        print(view)
        print("el obj es:")
        print( obj ) #el objeto será la data osea Comment , pero al dejarlo solo osea obj cogera al usuario. #!ojo: esto pq en el 
                                                                        #!serializador do comment tengo comentario_user 
        
        # print(obj.comentario_user)
        # print( obj.inmueble)
        # print( view)
        #*condición para q la lectura de cualquier usuario logeado o no logeado sea global osea q pueda consultar, osea es lo mismo
        #*q poner if request.method == 'GET'. lo de abajo se lee: si request.method está en el método get. 
        #para hacer esto:  if request.method in permissions.SAFE_METHODS hay q tener en cuenta el orden osea el chiquito delante
        #quiero decir si estoy buscando si una palabra aparece en un texto es asi: if palabra in texto y no puede ser al revéz 
        if request.method in permissions.SAFE_METHODS: #Safe method representa los metodos de tipo get
            return True
        #!tengo q cubir los demas metodos del view( clase de la vista ) pq sino no aparecen
        else: #si es otro metodo, osea un put, un delete
            #return obj.comentario_user == request.user#!si el usuario del objeto es el mismo q esta logeado actuamente pues dime q True
            #*abajo le agrege al return  para q devuleva True si es un usuario administrador
            return obj.comentario_user == request.user or request.user.is_staff
        
 
    


        
        
        #print(view.get_queryset())
        
        #*sino es un get y eso u post o put o delete pues q lea esto de abjo
        # if request.method == 'PUT':
        #     print("seeee")
        #     user = request.user
        #     comentario = Comment.objects.filter(comentario_user = user)

        #     if comentario:
        #         return True
        #     else:
        #         return False

        
            #comentario = Comment.objects.filter(user=usuario)
            # staff_permission = bool(request.user == usuario)
            # return staff_permission





#como lo hizo el
# class AdminComment(permissions.BasePermission): #la clase adminUser es del administrador(panel de control) de permisos de usuario

#     def has_object_permission(self, request, view, obj):
#         # print("el valor del request es")
#         # print(request) #<rest_framework.request.Request: OPTIONS '/tienda/edificacion/2/comentario'>
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         else:
#             return obj.comentario_user == request.user #el usuario de session fue el encargado de realizar ese comentario    





#repaso:
        
# from rest_framework.permissions import IsAdminUser
# class EdificacionListPermissions(IsAdminUser):

#     def has_permission(self, request, view):
        #*aqui no puse if request.method == 'GET' pq se supone q la clase en el view hereda del ListAPIView  esta solamente permite 
        #*el get por lo qhabia q registringir a los usuario q no estaban autheticados
#         if request.user.is_authenticated:
#             return True




            

            




        




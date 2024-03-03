from rest_framework.throttling import UserRateThrottle

class ComentarioCreateThrottling(UserRateThrottle): 

    scope = 'comentario-create'
    



class ComentarioListThrottling(UserRateThrottle):
    scope = 'comentario-list'
























             
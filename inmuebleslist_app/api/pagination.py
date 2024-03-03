from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class InmueblesPagination(PageNumberPagination):
    page_size = 1 
    page_query_param = 'p' 
    page_size_query_param = 'size'
    max_page_size = 10


class InmueblesLOPagination(LimitOffsetPagination):
    default_limit = 1 #


      



       


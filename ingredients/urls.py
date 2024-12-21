from django.urls import path
from .views import list_ingredient, get_ingredient_byid, get_ingredient_list_name, get_ingredient_name_by_id, post_ingredient, delete_ingredient, put_ingredient

urlpatterns = [
    path('list/', list_ingredient, name='list_ingredient'), 
    path('<int:ingredient_id>', get_ingredient_byid, name='get_ingredient_byid'), 
    path('list_name_ingredient/', get_ingredient_list_name, name='get_ingredient_list_name'), 
    path('ingredient_name/<int:ingredient_id>',get_ingredient_name_by_id, name="get_ingredient_name_by_id" ),
    path('add_ingredient/', post_ingredient, name="post_ingredient"), 
    path('put_ingredient/', put_ingredient, name="put_ingredient"), 
    path('delete_ingredient/<int:_id_ingredient>', delete_ingredient, name="delete_ingredient"), 
]

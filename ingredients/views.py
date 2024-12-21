from django.shortcuts import render
from django.http import HttpRequest, Http404, JsonResponse
from .models import Ingredient

def list_ingredient(request:HttpRequest): 
    try: 
        list_ingredient = Ingredient.objects.all().values()
    except: 
        raise Http404("No Ingredient available")

    return JsonResponse(list(list_ingredient), safe=False, status=200) 

def get_ingredient_byid(request:HttpRequest, ingredient_id): 
    try: 
        print(ingredient_id)
        ingredient= Ingredient.objects.get(id_ingredient=ingredient_id)
        ingredient_data = {
            "name": ingredient.name, 
            "image": ingredient.image_url, 
            "id_ingredient": ingredient.id_ingredient
        }
        print(ingredient)
    except: 
        raise Http404("Ingredient does not exists")
    return JsonResponse(ingredient_data, status=200)

def get_ingredient_list_name(request: HttpRequest): 
    try: 
        list_name_ingredient= Ingredient.objects.values_list('name', flat=True)
    except: 
        raise Http404("No Ingredient available")
    return JsonResponse(list(list_name_ingredient), safe=False, status=202)

def get_ingredient_name_by_id(request: HttpRequest, ingredient_id): 
    try: 
        ingredient= Ingredient.objects.get(id_ingredient=ingredient_id)
    except: 
        raise Http404("Ingredient does not exists")
    
    return JsonResponse(ingredient.name, safe=False, status=200)


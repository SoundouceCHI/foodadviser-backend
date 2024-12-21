from django.shortcuts import render
from django.http import HttpRequest, Http404, JsonResponse
from .models import Ingredient
import json 

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


def post_ingredient(request): 

    try:
        data = json.loads(request.body)
        id_ingredient = data.get('id_ingredient')
        name = data.get('name')
        image_url = data.get('image_url', '')

        if not id_ingredient or not name:
            return JsonResponse({"error": "Fields 'id_ingredient' and 'name' are required."}, status=400)

        ingredient, created = Ingredient.objects.get_or_create(
            id_ingredient=id_ingredient,
            defaults={'name': name, 'image_url': image_url}
        )

        if not created:
            return JsonResponse({"error": "Ingredient already exists."}, status=400)

        return JsonResponse({
            "message": "Ingredient created successfully",
            "ingredient": {
            "id_ingredient": ingredient.id_ingredient,
            "name": ingredient.name,
            "image_url": ingredient.image_url
            }
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)


def put_ingredient(request): 

    try:
        data = json.loads(request.body)
        id_ingredient = data.get('id_ingredient')
        data_name = data.get('name')
        data_image_url = data.get('image_url', '')

        if not id_ingredient or not data_name:
            return JsonResponse({"error": "Fields 'id_ingredient' and 'name' are required."}, status=400)

        rows_updated = Ingredient.objects.filter(id_ingredient=id_ingredient).update(name=data_name, image_url= data_image_url)

        if rows_updated == 0:
            return JsonResponse({"error": "Ingredient already exists."}, status=400)

        return JsonResponse({
            "message": "Ingredient updated successfully"
        }, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)


def delete_ingredient(request, _id_ingredient): 
    try:
        deleted_count, _ = Ingredient.objects.filter(id_ingredient=_id_ingredient).delete() 

        if deleted_count== 0:
            return JsonResponse({"error": "Ingredient not exists."}, status=400)

        return JsonResponse({
            "message": "Ingredient deleted successfully"
        }, status=200)
    except json.JSONDecodeError:
       return JsonResponse({"error": "Invalid JSON format."}, status=400)

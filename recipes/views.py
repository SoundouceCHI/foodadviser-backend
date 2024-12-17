from django.shortcuts import render
from django.http import JsonResponse
import requests

API_KEY = ''

def get_recipe(request, recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}&includeNutrition=true'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Unable to fetch recipe data"}, status=500)


def get_recipes_list(request):
    number = request.GET.get('number', 100)  

    # url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&query={query}&cuisine={cuisine}&diet={diet}&number={number}'
    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&number={number}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Unable to fetch recipes list"}, status=500)

from django.core.cache import cache
import requests
from django.http import JsonResponse
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')

def get_recipe(request, recipe_id):
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}&includeNutrition=true'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Unable to fetch recipe data"}, status=500)


def get_recipes_list(request):
    number = request.GET.get('number', 100)  

    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&number={number}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    elif response.status_code == 402:
        return JsonResponse({"error": "Daily points limit reached. Please try again tomorrow."}, status=402)
    else:
        return JsonResponse({"error": "Unable to fetch recipes list"}, status=500)



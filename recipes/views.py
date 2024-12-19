from django.core.cache import cache
import requests
from django.http import JsonResponse


# my first account
# API_KEY = '34bba94fff724a70b81a614c97a87016'
# my second account
API_KEY = '46b4b79dcc6c48b1a8d0687640f32afe'

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
    elif response.status_code == 402:
        return JsonResponse({"error": "Daily points limit reached. Please try again tomorrow."}, status=402)
    else:
        return JsonResponse({"error": "Unable to fetch recipes list"}, status=500)


# def get_recipes_list(request):
#     number = request.GET.get('number', 5)
#     cache_key = f"recipes_list_{number}"
#     cached_data = cache.get(cache_key)

#     if cached_data:
#         return JsonResponse(cached_data)

#     url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&number={number}'
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()
#         cache.set(cache_key, data, timeout=3600)  
#         return JsonResponse(data)
#     elif response.status_code == 402:
#         return JsonResponse({"error": "Daily points limit reached. Please try again tomorrow."}, status=402)
#     else:
#         return JsonResponse({"error": "Unable to fetch recipes list"}, status=response.status_code)





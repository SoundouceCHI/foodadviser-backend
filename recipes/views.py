from django.core.cache import cache
import requests
from django.http import JsonResponse
from dotenv import load_dotenv
import os
from .models import Recipe, Nutrition

load_dotenv()

api_key = os.getenv('API_KEY')

def get_recipe(request, recipe_id):
    cache_key = f"recipe_{recipe_id}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return JsonResponse(cached_data)

    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}&includeNutrition=true'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        cache.set(cache_key, data, timeout=3600)  # Cache the data for an hour
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Unable to fetch recipe data"}, status=500)


def get_recipes_list(request):
    number = request.GET.get('number', 100)

    # Si les données ne sont pas en cache, faites la requête à l'API
    url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&number={number}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lance une exception pour les réponses d'erreur HTTP
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Request failed: {str(e)}"}, status=500)

    if response.status_code == 200:
        data = response.json()
        
        # Sauvegarder les recettes (si nécessaire)
        for recipe in data.get('results', []):
            save_recipe(recipe)

        return JsonResponse(data)
    elif response.status_code == 402:
        return JsonResponse({"error": "Daily points limit reached. Please try again tomorrow."}, status=402)
    else:
        return JsonResponse({"error": "Unable to fetch recipes list"}, status=500)

def save_recipe(recipe):
    recipe_id = recipe.get('id')
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}&includeNutrition=true'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        steps = [
            {"number": step['number'], "step": step['step']}
            for instruction in data.get('analyzedInstructions', [])
            for step in instruction.get('steps', [])
        ]
        
        recipe, created = Recipe.objects.get_or_create(
            id_recipe=recipe_id,
            defaults={
                'title': data.get('title', ''),
                'image_url': data.get('image', ''),
                'instructions': data.get('instructions', ''),
                'steps': steps,
                'servings': data.get('servings', 1),
                'ready_in_minutes': data.get('readyInMinutes', 0),
                'vegetarian': data.get('vegetarian', False),
                'vegan': data.get('vegan', False),
                'very_popular': data.get('veryPopular', False),
                'preparation_minutes': data.get('preparationMinutes', None),
                'cooking_minutes': data.get('cookingMinutes', None),
                'health_score': data.get('healthScore', None),
            }
        )

        if created:
            nutrition_data = data.get('nutrition', {}).get('nutrients', [])
            nutrition_values = {nutrient['name']: nutrient['amount'] for nutrient in nutrition_data}

            Nutrition.objects.create(
                recipe=recipe,
                calories=nutrition_values.get('Calories', None),
                protein=nutrition_values.get('Protein', None),
                fat=nutrition_values.get('Fat', None),
                carbohydrates=nutrition_values.get('Carbohydrates', None),
                sugar=nutrition_values.get('Sugar', None),
                fiber=nutrition_values.get('Fiber', None),
                sodium=nutrition_values.get('Sodium', None),
            )

        return JsonResponse({
            "message": "Recipe saved successfully!" if created else "Recipe already exists in the database!"
        })
    else:
        return JsonResponse({"error": "Unable to fetch recipe data"}, status=response.status_code)
    

def getRecipesSuggestionList(request): 
    ingredients = request.GET.get('list', '')
    number= int(request.GET.get('number', 8))
    print("Ingredients:", ingredients)
    print("Number:", number)

    if not ingredients:
            return JsonResponse({"error": "Missing 'list' parameter"}, status=400)
    
    url=(
            f'https://api.spoonacular.com/recipes/findByIngredients'
            f'?ingredients={ingredients}&number={number}&apiKey={api_key}'
        )
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, safe=False)
    
    elif response.status_code == 402:
        return JsonResponse({"error": "Daily points limit reached. Please try again tomorrow."}, status=402)
    else:
        return JsonResponse({"error": "Unable to fetch recipes list"}, status=500)
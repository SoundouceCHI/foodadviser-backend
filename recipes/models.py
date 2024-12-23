from django.db import models

class Recipe(models.Model):
    id_recipe = models.IntegerField(unique=True)  
    title = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True) 
    steps = models.JSONField(null=True, blank=True) 
    servings = models.IntegerField(null=True, blank=True)
    ready_in_minutes = models.IntegerField(null=True, blank=True)
    vegetarian = models.BooleanField(default=False)  
    vegan = models.BooleanField(default=False)       
    very_popular = models.BooleanField(default=False) 
    preparation_minutes = models.IntegerField(null=True, blank=True)  
    cooking_minutes = models.IntegerField(null=True, blank=True)     
    health_score = models.FloatField(null=True, blank=True)           

    def __str__(self):
        return self.title

class Nutrition(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name='nutrition')
    calories = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)    
    carbohydrates = models.FloatField(null=True, blank=True)  
    sugar = models.FloatField(null=True, blank=True)    
    fiber = models.FloatField(null=True, blank=True)    
    sodium = models.FloatField(null=True, blank=True)   

    def __str__(self):
        return f"Nutrition for {self.recipe.title}"
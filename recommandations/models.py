from django.db import models
from django.contrib.auth.models import User  
from recipes.models import Recipe

class UserRecipeViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_views')
    recipe_title = models.CharField(max_length=255, null=False)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe_title')  

    def __str__(self):
        return f"User ID: {self.user_id} viewed Recipe: {self.recipe_title} on {self.viewed_at}"

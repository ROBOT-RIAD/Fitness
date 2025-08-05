from django.db import models

 
class Recipe(models.Model):
    unique_id = models.CharField(max_length=100, unique=True,null=True, blank=True,help_text="same RecipeSpanish data")
    image = models.ImageField(upload_to='media/recipes/', null=True, blank=True)
    recipe_name = models.CharField(max_length=255)
    recipe_type = models.CharField(max_length=50)  # Example: Vegetarian, Non-Vegetarian, etc.
    for_time = models.CharField(max_length=50)     # Example: Breakfast, Lunch, Dinner
    tag = models.CharField(max_length=200, blank=True)  # Example: Spicy, Quick, Healthy
    calories = models.DecimalField(max_digits=12, decimal_places=2)
    carbs = models.DecimalField(max_digits=8, decimal_places=2)
    protein = models.DecimalField(max_digits=8, decimal_places=2)
    fat = models.DecimalField(max_digits=8, decimal_places=2)
    making_time = models.DurationField(help_text="Time needed to make the recipe (hh:mm:ss)")
    time = models.DurationField(help_text="Additional time or total time (hh:mm:ss)")
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    category = models.CharField(max_length=50)     # Example: Dessert, Main, Snack
    ingredients = models.TextField(help_text="List ingredients separated by commas or lines.")
    instructions = models.TextField(help_text="Step-by-step cooking instructions.")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return (
            f"Unique ID: {self.unique_id}, "
            f"Name: {self.recipe_name}, "
            f"Type: {self.recipe_type}, "
            f"Tag: {self.tag}, "
            f"Calories: {self.calories}, "
            f"Carbs: {self.carbs}, "
            f"Protein: {self.protein}, "
            f"Fat: {self.fat}, "
            f"Making Time: {self.making_time}, "
            f"Time: {self.time}, "
            f"Ratings: {self.ratings}, "
            f"Category: {self.category}, "
            f"For: {self.for_time}, "
            f"Ingredients: {self.ingredients[:30]}..., "
            f"Instructions: {self.instructions[:30]}..."
        )




class RecipeSpanish(models.Model):
    unique_id = models.CharField(max_length=100 ,unique=True,null=True, blank=True, help_text="same Recipe data")
    image = models.ImageField(upload_to='media/recipes/', null=True, blank=True)
    recipe_name = models.CharField(max_length=255)
    recipe_type = models.CharField(max_length=50)
    for_time = models.CharField(max_length=50)
    tag = models.CharField(max_length=200, blank=True)
    calories = models.DecimalField(max_digits=12, decimal_places=2)
    carbs = models.DecimalField(max_digits=8, decimal_places=2)
    protein = models.DecimalField(max_digits=8, decimal_places=2)
    fat = models.DecimalField(max_digits=8, decimal_places=2)
    making_time = models.DurationField(help_text="Tiempo necesario para preparar la receta (hh:mm:ss)")
    time = models.DurationField(help_text="Tiempo adicional o total (hh:mm:ss)")
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    category = models.CharField(max_length=50)
    ingredients = models.TextField(help_text="Lista de ingredientes separados por comas o líneas.")
    instructions = models.TextField(help_text="Instrucciones paso a paso para cocinar.")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return (
            f"Unique ID: {self.unique_id}, "
            f"Name: {self.recipe_name}, "
            f"Type: {self.recipe_type}, "
            f"Tag: {self.tag}, "
            f"Calories: {self.calories}, "
            f"Carbs: {self.carbs}, "
            f"Protein: {self.protein}, "
            f"Fat: {self.fat}, "
            f"Making Time: {self.making_time}, "
            f"Time: {self.time}, "
            f"Ratings: {self.ratings}, "
            f"Category: {self.category}, "
            f"For: {self.for_time}, "
            f"Ingredients: {self.ingredients[:30]}..., "
            f"Instructions: {self.instructions[:30]}..."
        )

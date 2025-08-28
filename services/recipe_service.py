from typing import List, Optional
from models import Recipe, RecipeRequest, RecipeResponse, ErrorResponse
from services.gemini_service import GeminiService

class RecipeService:
    """Service for handling recipe-related business logic"""
    
    def __init__(self):
        self.gemini_service = GeminiService()
    
    async def generate_recipes_from_ingredients(self, request: RecipeRequest) -> RecipeResponse:
        """Generate recipes based on available ingredients"""
        try:
            # Validate request
            if not request.ingredients:
                return RecipeResponse(
                    recipes=[],
                    success=False,
                    message="No ingredients provided"
                )
            
            # Check if we have at least one valid ingredient
            valid_ingredients = [ing for ing in request.ingredients if ing.strip()]
            if not valid_ingredients:
                return RecipeResponse(
                    recipes=[],
                    success=False,
                    message="No valid ingredients found"
                )
            
            # Generate recipes using Gemini AI
            response = self.gemini_service.generate_recipes(valid_ingredients)
            
            # If generation failed, return error
            if not response.success:
                return response
            
            # Validate that we got some recipes
            if not response.recipes:
                return RecipeResponse(
                    recipes=[],
                    success=False,
                    message="No recipes could be generated with the provided ingredients"
                )
            
            return response
            
        except Exception as e:
            return RecipeResponse(
                recipes=[],
                success=False,
                message=f"An error occurred while generating recipes: {str(e)}"
            )
    
    def validate_ingredients(self, ingredients: List[str]) -> tuple[bool, Optional[str]]:
        """Validate ingredients list"""
        if not ingredients:
            return False, "Ingredients list cannot be empty"
        
        if len(ingredients) < 1:
            return False, "At least one ingredient is required"
        
        # Check for very long ingredient names
        for ingredient in ingredients:
            if len(ingredient.strip()) > 100:
                return False, f"Ingredient '{ingredient}' is too long"
        
        return True, None
    
    def sanitize_ingredients(self, ingredients: List[str]) -> List[str]:
        """Clean and normalize ingredient names"""
        sanitized = []
        for ingredient in ingredients:
            # Remove extra whitespace and convert to lowercase
            cleaned = ingredient.strip().lower()
            if cleaned and len(cleaned) <= 100:
                sanitized.append(cleaned)
        return sanitized
    
    def get_recipe_summary(self, recipes: List[Recipe]) -> dict:
        """Get a summary of generated recipes"""
        if not recipes:
            return {}
        
        total_calories = sum(recipe.nutrition.calories for recipe in recipes)
        avg_calories = total_calories // len(recipes)
        
        difficulty_counts = {}
        for recipe in recipes:
            difficulty = recipe.difficulty.lower()
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        
        return {
            "total_recipes": len(recipes),
            "average_calories": avg_calories,
            "difficulty_distribution": difficulty_counts,
            "cooking_times": [recipe.cookingTime for recipe in recipes]
        }
    
    def test_service_health(self) -> dict:
        """Test if all services are working properly"""
        try:
            gemini_working = self.gemini_service.test_connection()
            
            return {
                "status": "healthy" if gemini_working else "degraded",
                "services": {
                    "gemini_ai": "operational" if gemini_working else "unavailable"
                },
                "timestamp": "2024-01-01T00:00:00Z"  # You can use datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "services": {
                    "gemini_ai": "error"
                },
                "error": str(e),
                "timestamp": "2024-01-01T00:00:00Z"
            }

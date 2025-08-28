from pydantic import BaseModel, Field, validator
from typing import List, Optional

class RecipeRequest(BaseModel):
    """Request model for recipe generation"""
    ingredients: List[str] = Field(..., description="List of available ingredients")
    
    @validator('ingredients')
    def validate_ingredients(cls, v):
        if not v:
            raise ValueError('Ingredients list cannot be empty')
        if len(v) < 1:
            raise ValueError('At least one ingredient is required')
        return [ingredient.strip().lower() for ingredient in v if ingredient.strip()]

class NutritionInfo(BaseModel):
    """Nutritional information for a recipe"""
    calories: int = Field(..., description="Calories per serving")
    protein: str = Field(..., description="Protein content (e.g., '12g')")
    carbs: str = Field(..., description="Carbohydrate content (e.g., '60g')")

class Recipe(BaseModel):
    """Individual recipe model"""
    name: str = Field(..., description="Recipe name")
    ingredients: List[str] = Field(..., description="List of ingredients needed")
    instructions: List[str] = Field(..., description="Step-by-step cooking instructions")
    cookingTime: str = Field(..., description="Estimated cooking time (e.g., '20 minutes')")
    difficulty: str = Field(..., description="Difficulty level: Easy, Medium, or Hard")
    nutrition: NutritionInfo = Field(..., description="Nutritional information")

class RecipeResponse(BaseModel):
    """Response model for recipe generation"""
    recipes: List[Recipe] = Field(..., description="List of generated recipes")
    success: bool = Field(True, description="Whether the request was successful")
    message: Optional[str] = Field(None, description="Additional information or error message")

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(False, description="Request was not successful")
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")

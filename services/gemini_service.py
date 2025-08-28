import os
import json
import google.generativeai as genai
from typing import List, Dict, Any
from models import Recipe, RecipeResponse, ErrorResponse

class GeminiService:
    """Service for interacting with Google Gemini AI"""
    
    def __init__(self):
        api_key = os.getenv('gemini_key')
        if not api_key:
            raise ValueError("gemini_key environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def generate_recipes(self, ingredients: List[str]) -> RecipeResponse:
        """Generate recipes using Gemini AI based on available ingredients"""
        try:
            # Create structured prompt for consistent JSON output
            prompt = self._create_recipe_prompt(ingredients)
            
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse and validate the response
            recipes = self._parse_ai_response(response.text)
            
            return RecipeResponse(
                recipes=recipes,
                success=True,
                message=f"Generated {len(recipes)} recipes using your ingredients"
            )
            
        except Exception as e:
            # Return error response if something goes wrong
            return RecipeResponse(
                recipes=[],
                success=False,
                message=f"Failed to generate recipes: {str(e)}"
            )
    
    def _create_recipe_prompt(self, ingredients: List[str]) -> str:
        """Create a structured prompt for recipe generation"""
        ingredients_str = ", ".join(ingredients)
        
        prompt = f"""
Generate 2-3 creative recipe suggestions using these ingredients: {ingredients_str}

Requirements:
- Each recipe must use the provided ingredients as primary components
- Include estimated cooking time and difficulty level
- Provide realistic nutritional information (calories, protein, carbs)
- Format response as valid JSON only
- Be creative but practical with cooking instructions

Response format (return ONLY valid JSON):
{{
  "recipes": [
    {{
      "name": "Recipe Name",
      "ingredients": ["ingredient1", "ingredient2", "additional_ingredients_needed"],
      "instructions": ["step1", "step2", "step3"],
      "cookingTime": "X minutes",
      "difficulty": "Easy/Medium/Hard",
      "nutrition": {{
        "calories": X,
        "protein": "Xg",
        "carbs": "Xg"
      }}
    }}
  ]
}}

Important: Return ONLY the JSON response, no additional text or explanations.
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> List[Recipe]:
        """Parse the AI response and extract recipe data"""
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Try to find JSON content if there's extra text
            if "```json" in cleaned_text:
                start = cleaned_text.find("```json") + 7
                end = cleaned_text.rfind("```")
                cleaned_text = cleaned_text[start:end].strip()
            elif "```" in cleaned_text:
                start = cleaned_text.find("```") + 3
                end = cleaned_text.rfind("```")
                cleaned_text = cleaned_text[start:end].strip()
            
            # Parse JSON
            data = json.loads(cleaned_text)
            
            # Validate and convert to Recipe objects
            recipes = []
            for recipe_data in data.get("recipes", []):
                try:
                    recipe = Recipe(**recipe_data)
                    recipes.append(recipe)
                except Exception as e:
                    print(f"Warning: Skipping invalid recipe: {e}")
                    continue
            
            return recipes
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response_text}")
            raise ValueError("Failed to parse AI response as JSON")
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            raise ValueError(f"Failed to process AI response: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test if Gemini API is working"""
        try:
            test_prompt = "Say 'Hello' in one word."
            response = self.model.generate_content(test_prompt)
            return "Hello" in response.text
        except Exception:
            return False

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from models import RecipeRequest, RecipeResponse, ErrorResponse
from services.recipe_service import RecipeService
from services.storage_service import StorageService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Smart Recipe Analyzer",
    description="AI-powered recipe generator based on available ingredients",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
recipe_service = RecipeService()
storage_service = StorageService()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML page"""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Smart Recipe Analyzer</h1><p>templates/index.html not found</p>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Smart Recipe Analyzer"}

@app.get("/api/health")
async def api_health_check():
    """Detailed API health check"""
    return recipe_service.test_service_health()

@app.post("/api/recipes/generate", response_model=RecipeResponse)
async def generate_recipes(request: RecipeRequest):
    """Generate recipes based on available ingredients"""
    try:
        # Log the incoming request
        print(f"🔍 Backend - Received request: {request}")
        print(f"📥 Backend - Ingredients received: {request.ingredients}")
        print(f"📊 Backend - Request type: {type(request)}")
        print(f"📋 Backend - Request dict: {request.dict()}")
        
        # Validate ingredients
        is_valid, error_message = recipe_service.validate_ingredients(request.ingredients)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)
        
        # Sanitize ingredients
        sanitized_ingredients = recipe_service.sanitize_ingredients(request.ingredients)
        if not sanitized_ingredients:
            raise HTTPException(status_code=400, detail="No valid ingredients found after sanitization")
        
        # Create new request with sanitized ingredients
        sanitized_request = RecipeRequest(ingredients=sanitized_ingredients)
        
        # Generate recipes
        response = await recipe_service.generate_recipes_from_ingredients(sanitized_request)
        
        if not response.success:
            raise HTTPException(status_code=500, detail=response.message)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/recipes/sample")
async def get_sample_recipes():
    """Get sample recipes for testing (doesn't require API key)"""
    sample_recipes = [
        {
            "name": "Sample Pasta Dish",
            "ingredients": ["pasta", "garlic", "olive oil", "parmesan"],
            "instructions": [
                "Boil pasta according to package instructions",
                "Sauté minced garlic in olive oil",
                "Toss pasta with garlic oil and parmesan"
            ],
            "cookingTime": "15 minutes",
            "difficulty": "Easy",
            "nutrition": {
                "calories": 400,
                "protein": "12g",
                "carbs": "65g"
            }
        }
    ]
    
    return RecipeResponse(
        recipes=sample_recipes,
        success=True,
        message="Sample recipe for testing purposes"
    )

@app.get("/api/interactions/all")
async def get_all_interactions():
    """Get all stored user interactions"""
    interactions = storage_service.get_all_interactions()
    return {
        "interactions": interactions,
        "total": len(interactions)
    }

@app.get("/api/interactions/recent")
async def get_recent_interactions(limit: int = 10):
    """Get recent user interactions"""
    interactions = storage_service.get_recent_interactions(limit)
    return {
        "interactions": interactions,
        "total": len(interactions),
        "limit": limit
    }

@app.get("/api/interactions/stats")
async def get_interaction_stats():
    """Get statistics about stored interactions"""
    stats = storage_service.get_storage_stats()
    return stats

@app.get("/api/interactions/{interaction_id}")
async def get_interaction(interaction_id: str):
    """Get a specific interaction by ID"""
    interaction = storage_service.get_interaction_by_id(interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors"""
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "path": request.url.path}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle 500 errors"""
    from fastapi.responses import JSONResponse
    error_detail = str(exc) if hasattr(exc, '__str__') else "Unknown error"
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": error_detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle any other exceptions"""
    from fastapi.responses import JSONResponse
    error_detail = str(exc) if hasattr(exc, '__str__') else "Unknown error"
    return JSONResponse(
        status_code=500,
        content={"error": "Unexpected error", "detail": error_detail}
    )

if __name__ == "__main__":
    import uvicorn
    
    # Check if Gemini API key is available
    if not os.getenv('gemini_key'):
        print("Warning: gemini_key not found in environment variables")
        print("The application will start but recipe generation will fail")
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

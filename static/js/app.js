// Smart Recipe Analyzer - Frontend JavaScript
class RecipeAnalyzer {
    constructor() {
        this.apiBaseUrl = window.location.origin;
        this.currentRecipes = [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Form submission
        const form = document.getElementById('recipeForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Sample ingredient buttons
        const sampleBtns = document.querySelectorAll('.sample-btn');
        sampleBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleSampleClick(e));
        });

        // New search button
        const newSearchBtn = document.getElementById('newSearchBtn');
        if (newSearchBtn) {
            newSearchBtn.addEventListener('click', () => this.resetToInput());
        }

        // Retry button
        const retryBtn = document.getElementById('retryBtn');
        if (retryBtn) {
            retryBtn.addEventListener('click', () => this.retryRequest());
        }

        // Input validation
        const ingredientsInput = document.getElementById('ingredientsInput');
        if (ingredientsInput) {
            ingredientsInput.addEventListener('input', (e) => this.validateInput(e));
        }
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const ingredientsInput = document.getElementById('ingredientsInput');
        const ingredients = ingredientsInput.value.trim();
        
        if (!ingredients) {
            this.showError('Please enter some ingredients', 'No ingredients provided');
            return;
        }

        // Parse ingredients
        const ingredientsList = this.parseIngredients(ingredients);
        
        if (ingredientsList.length === 0) {
            this.showError('Please enter valid ingredients', 'Invalid ingredients format');
            return;
        }

        // Show loading state
        this.showLoading();
        
        try {
            const response = await this.generateRecipes(ingredientsList);
            this.handleRecipeResponse(response);
        } catch (error) {
            console.error('Error generating recipes:', error);
            this.showError('Failed to generate recipes', error.message || 'An unexpected error occurred');
        }
    }

    parseIngredients(ingredientsText) {
        return ingredientsText
            .split(',')
            .map(ingredient => ingredient.trim())
            .filter(ingredient => ingredient.length > 0);
    }

    validateInput(e) {
        const input = e.target;
        const value = input.value.trim();
        
        if (value.length > 500) {
            input.setCustomValidity('Ingredients list is too long (max 500 characters)');
        } else {
            input.setCustomValidity('');
        }
    }

    async generateRecipes(ingredients) {
        // Log the ingredients being sent
        console.log('🔍 Frontend - Ingredients to send:', ingredients);
        
        const requestBody = { ingredients };
        console.log('📤 Frontend - Request body (JSON):', JSON.stringify(requestBody, null, 2));
        
        const response = await fetch(`${this.apiBaseUrl}/api/recipes/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('📥 Frontend - Response received:', responseData);
        console.log('📊 Frontend - Response type:', typeof responseData);
        console.log('📋 Frontend - Response keys:', Object.keys(responseData));
        
        return responseData;
    }

    handleRecipeResponse(response) {
        if (response.success && response.recipes && response.recipes.length > 0) {
            this.currentRecipes = response.recipes;
            this.displayRecipes(response.recipes);
            this.showResults();
        } else {
            this.showError(
                'No recipes generated', 
                response.message || 'The AI couldn\'t generate recipes with your ingredients'
            );
        }
    }

    displayRecipes(recipes) {
        const container = document.getElementById('recipesContainer');
        if (!container) return;

        container.innerHTML = '';
        
        recipes.forEach(recipe => {
            const recipeElement = this.createRecipeElement(recipe);
            container.appendChild(recipeElement);
        });
    }

    createRecipeElement(recipe) {
        const template = document.getElementById('recipeTemplate');
        if (!template) return document.createElement('div');

        const clone = template.content.cloneNode(true);
        
        // Set recipe name
        const nameElement = clone.querySelector('.recipe-name');
        if (nameElement) nameElement.textContent = recipe.name;
        
        // Set cooking time
        const timeElement = clone.querySelector('.time-text');
        if (timeElement) timeElement.textContent = recipe.cookingTime;
        
        // Set difficulty
        const difficultyElement = clone.querySelector('.difficulty-text');
        if (difficultyElement) difficultyElement.textContent = recipe.difficulty;
        
        // Set ingredients
        const ingredientsList = clone.querySelector('.ingredients-list');
        if (ingredientsList) {
            recipe.ingredients.forEach(ingredient => {
                const li = document.createElement('li');
                li.textContent = ingredient;
                ingredientsList.appendChild(li);
            });
        }
        
        // Set instructions
        const instructionsList = clone.querySelector('.instructions-list');
        if (instructionsList) {
            recipe.instructions.forEach(instruction => {
                const li = document.createElement('li');
                li.textContent = instruction;
                instructionsList.appendChild(li);
            });
        }
        
        // Set nutrition
        const caloriesElement = clone.querySelector('.nutrition-value.calories');
        if (caloriesElement) caloriesElement.textContent = recipe.nutrition.calories;
        
        const proteinElement = clone.querySelector('.nutrition-value.protein');
        if (proteinElement) proteinElement.textContent = recipe.nutrition.protein;
        
        const carbsElement = clone.querySelector('.nutrition-value.carbs');
        if (carbsElement) carbsElement.textContent = recipe.nutrition.carbs;
        
        return clone;
    }

    handleSampleClick(e) {
        const ingredients = e.currentTarget.dataset.ingredients;
        const ingredientsInput = document.getElementById('ingredientsInput');
        
        if (ingredientsInput) {
            ingredientsInput.value = ingredients;
            // Trigger form submission
            const form = document.getElementById('recipeForm');
            if (form) {
                form.dispatchEvent(new Event('submit'));
            }
        }
    }

    showLoading() {
        this.hideAllSections();
        const loadingSection = document.getElementById('loadingSection');
        if (loadingSection) {
            loadingSection.classList.remove('hidden');
        }
    }

    showResults() {
        this.hideAllSections();
        const resultsSection = document.getElementById('resultsSection');
        if (resultsSection) {
            resultsSection.classList.remove('hidden');
        }
    }

    showError(title, message) {
        this.hideAllSections();
        
        const errorSection = document.getElementById('errorSection');
        const errorTitle = document.getElementById('errorTitle');
        const errorMessage = document.getElementById('errorMessage');
        
        if (errorSection && errorTitle && errorMessage) {
            errorTitle.textContent = title;
            errorMessage.textContent = message;
            errorSection.classList.remove('hidden');
        }
    }

    hideAllSections() {
        const sections = [
            'loadingSection',
            'resultsSection', 
            'errorSection'
        ];
        
        sections.forEach(sectionId => {
            const section = document.getElementById(sectionId);
            if (section) {
                section.classList.add('hidden');
            }
        });
    }

    resetToInput() {
        this.hideAllSections();
        this.currentRecipes = [];
        
        // Clear form
        const form = document.getElementById('recipeForm');
        if (form) {
            form.reset();
        }
        
        // Show input section (it's always visible by default)
        const inputSection = document.querySelector('.input-section');
        if (inputSection) {
            inputSection.scrollIntoView({ behavior: 'smooth' });
        }
    }

    retryRequest() {
        if (this.currentRecipes.length > 0) {
            // Retry with the same ingredients
            this.displayRecipes(this.currentRecipes);
            this.showResults();
        } else {
            // Go back to input
            this.resetToInput();
        }
    }

    // Utility method to show success message
    showSuccess(message) {
        // Create a temporary success notification
        const notification = document.createElement('div');
        notification.className = 'success-notification';
        notification.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }

    // Method to handle API health check
    async checkApiHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/health`);
            const health = await response.json();
            
            if (health.status === 'healthy') {
                console.log('API is healthy:', health);
            } else {
                console.warn('API health check failed:', health);
            }
        } catch (error) {
            console.error('API health check error:', error);
        }
    }

    // Method to get sample recipes (for testing without API key)
    async getSampleRecipes() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/recipes/sample`);
            const data = await response.json();
            
            if (data.success) {
                this.currentRecipes = data.recipes;
                this.displayRecipes(data.recipes);
                this.showResults();
            }
        } catch (error) {
            console.error('Error getting sample recipes:', error);
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Create global instance
    window.recipeAnalyzer = new RecipeAnalyzer();
    
    // Check API health on load
    setTimeout(() => {
        window.recipeAnalyzer.checkApiHealth();
    }, 1000);
    
    // Add some CSS for success notifications
    const style = document.createElement('style');
    style.textContent = `
        .success-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #27ae60;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .success-notification i {
            font-size: 1.2rem;
        }
    `;
    document.head.appendChild(style);
    
    console.log('Smart Recipe Analyzer initialized! 🍳');
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RecipeAnalyzer;
}

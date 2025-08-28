# 🍳 Smart Recipe Analyzer

A web application that uses AI to generate recipe suggestions based on available ingredients, complete with nutritional analysis and cooking instructions.

## ✨ Features

- **AI-Powered Recipe Generation**: Get creative recipe suggestions using Google Gemini AI
- **Smart Ingredient Analysis**: Input any ingredients you have and get multiple recipe options
- **Nutritional Information**: Detailed breakdown of calories, protein, and carbs
- **Cooking Instructions**: Step-by-step cooking directions with time estimates
- **Difficulty Levels**: Recipes categorized by cooking complexity
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Processing**: Instant recipe generation with loading states

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-recipe-analyzer.git
   cd smart-recipe-analyzer
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the application**
   ```bash
   # Start the backend
   uvicorn main:app --reload
   
   # Open index.html in your browser
   # Or serve it using a local server
   python -m http.server 8000
   ```

6. **Access the application**
   - Frontend: `http://localhost:8000`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

## 🏗️ Project Structure

```
smart-recipe-analyzer/
├── main.py                 # FastAPI backend server
├── models.py              # Pydantic data models
├── services/
│   ├── __init__.py
│   ├── gemini_service.py  # Gemini AI integration
│   └── recipe_service.py  # Recipe processing logic
├── static/
│   ├── css/
│   │   └── style.css      # Main stylesheet
│   └── js/
│       └── app.js         # Frontend JavaScript
├── templates/
│   └── index.html         # Main HTML template
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🔧 API Endpoints

### POST `/api/recipes/generate`

Generate recipes based on ingredients.

**Request Body:**
```json
{
  "ingredients": ["chicken", "rice", "vegetables"]
}
```

**Response:**
```json
{
  "recipes": [
    {
      "name": "Chicken Fried Rice",
      "ingredients": ["chicken", "rice", "vegetables", "soy sauce"],
      "instructions": [
        "Cook rice according to package instructions",
        "Sauté chicken until golden brown",
        "Add vegetables and stir-fry",
        "Combine with rice and soy sauce"
      ],
      "cookingTime": "25 minutes",
      "difficulty": "Medium",
      "nutrition": {
        "calories": 380,
        "protein": "28g",
        "carbs": "45g"
      }
    }
  ]
}
```

## 🎯 LLM Integration

### Prompt Engineering

The application uses structured prompts to ensure consistent recipe generation:

```
Generate 2-3 recipe suggestions using these ingredients: [INGREDIENTS]

Requirements:
- Each recipe must use the provided ingredients
- Include estimated cooking time and difficulty level
- Provide basic nutritional information (calories, protein, carbs)
- Format response as valid JSON

Response format:
{
  "recipes": [
    {
      "name": "Recipe Name",
      "ingredients": ["ingredient1", "ingredient2"],
      "instructions": ["step1", "step2"],
      "cookingTime": "X minutes",
      "difficulty": "Easy/Medium/Hard",
      "nutrition": {
        "calories": X,
        "protein": "Xg",
        "carbs": "Xg"
      }
    }
  ]
}
```

### Gemini API Configuration

- **Model**: `gemini-pro` for text generation
- **Temperature**: 0.7 for creative but consistent output
- **Max Tokens**: 2000 for comprehensive recipe details

## 🎨 Frontend Features

- **Responsive Design**: Mobile-first approach with Bootstrap-like styling
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Form Validation**: Client-side input validation
- **Modern UI**: Clean, intuitive interface

## 🔒 Security & Validation

- **Input Sanitization**: Prevents XSS and injection attacks
- **Request Validation**: Ensures ingredients list is not empty
- **API Rate Limiting**: Prevents abuse
- **Environment Variables**: Secure API key management

## 🚀 Deployment

### Local Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Testing

```bash
# Run backend tests
pytest

# Run frontend tests (if implemented)
npm test

# Manual testing
# 1. Start the backend
# 2. Open index.html in browser
# 3. Test with various ingredient combinations
```

## 📱 Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for recipe generation
- FastAPI for the robust backend framework
- Pydantic for data validation
- The open-source community for inspiration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/smart-recipe-analyzer/issues) page
2. Create a new issue with detailed information
3. Contact the development team

## 🔮 Future Enhancements

- [ ] Recipe rating system
- [ ] Dietary restrictions filtering
- [ ] Ingredient substitutions
- [ ] Recipe history storage
- [ ] Image generation using DALL-E
- [ ] User accounts and favorites
- [ ] Recipe sharing functionality
- [ ] Mobile app version

---

**Happy Cooking! 🍽️**

import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDXRbrC7qxKwEiKRj0SCowcboH08IlNtA4")  # Replace with actual API key

# Initialize Gemini model
llm = genai.GenerativeModel("gemini-1.5-pro-latest")

# Database connection
DATABASE_URL = "sqlite:///budget_analysis.db"
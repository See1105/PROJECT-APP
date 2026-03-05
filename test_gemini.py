import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

try:
    print("Models found:")
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    for m in models:
        print(f" - {m}")
    
    test_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models else (models[0] if models else None)
    
    if test_model:
        print(f"\nTesting with {test_model}...")
        model = genai.GenerativeModel(test_model)
        response = model.generate_content("Say hello")
        print(f"Response: {response.text}")
    else:
        print("No suitable models found.")
except Exception as e:
    print(f"Error: {str(e)}")

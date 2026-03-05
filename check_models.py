import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

with open('models_list.txt', 'w') as f:
    try:
        f.write("Models found:\n")
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for m in models:
            f.write(f" - {m}\n")
        
        # Test a few models
        for test_model in ['models/gemini-1.5-flash', 'models/gemini-2.0-flash', 'models/gemini-2.5-flash']:
            if test_model in models:
                f.write(f"\nTesting {test_model}...\n")
                model = genai.GenerativeModel(test_model)
                response = model.generate_content("Say hello")
                f.write(f"Response: {response.text}\n")
            else:
                f.write(f"\n{test_model} NOT in list.\n")
    except Exception as e:
        f.write(f"Error: {str(e)}\n")

print("Done writing to models_list.txt")

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

with open('test_2_5.txt', 'w') as f:
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say hello")
        f.write(f"Response: {response.text}\n")
    except Exception as e:
        f.write(f"Error testing gemini-2.5-flash: {str(e)}\n")

print("Done")

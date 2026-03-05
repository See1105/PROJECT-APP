import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# This is a bit tricky since it requires a session/login.
# Let's just test the model directly again in a way that mimics the view.

import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    system_prompt = "You are a helpful AI Study Buddy."
    model = genai.GenerativeModel('gemini-flash-lite-latest', system_instruction=system_prompt)
    response = model.generate_content("Explain the concept of inheritance in Python.")
    print("Success! AI Response received.")
    print(f"Sample: {response.text[:100]}...")
except Exception as e:
    print(f"Error: {e}")

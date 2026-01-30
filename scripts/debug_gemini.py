import google.generativeai as genai
import os
import streamlit as st

import toml
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    try:
        secrets = toml.load(".streamlit/secrets.toml")
        api_key = secrets.get("GOOGLE_API_KEY")
    except:
        api_key = os.getenv("GOOGLE_API_KEY")

print(f"API Key present: {bool(api_key)}")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    print("Sending prompt to gemini-3-flash-preview...")
    try:
        response = model.generate_content("Hello, can you hear me?", stream=True)
        text = ""
        for chunk in response:
            print(f"Chunk received: {chunk.text}")
            text += chunk.text
        print(f"Final text: {text}")
    except Exception as e:
        print(f"Error: {e}")

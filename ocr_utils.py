import google.generativeai as genai
import json
import os
from PIL import Image
import streamlit as st
import re

def configure_genai():
    """Configures the Gemini API key from Streamlit secrets or environment variables."""
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except (FileNotFoundError, KeyError):
        api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("Google API Key not found in secrets.toml or environment variables.")
    
    genai.configure(api_key=api_key)

def extract_review_data(image):
    """
    Sends an image to Gemini 1.5 Flash to extract review data.
    Returns a dictionary with Username, Date, Rating, and Content.
    """
    configure_genai()
    
    # Using gemini-3-flash-preview as requested
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = """
    Analyze this image of a customer review. Extract the following information into a JSON object:
    - user_name: The name of the reviewer.
    - review_date: The date of the review. If format is MM/DD, convert to MM-DD. If year is missing, ALWAYS assume 2026.
    - rating_overall: The numeric rating (e.g., 4.5). Count ONLY stars colored in ORANGE. Do NOT count GREY stars. Count half stars if they are orange.
    - rating_taste: Rating for taste/food quality if present (float).
    - rating_env: Rating for environment/atmosphere if present (float).
    - rating_service: Rating for service if present (float).
    - rating_value: Rating for value/price if present (float).
    - content: The full text content of the review. REMOVE all emojis from the text. IMPORTANT: Ignore any text that appears to be a "Merchant Reply", "Response from Owner", or similar, usually located at the bottom of the review or in a different color/box. Extract ONLY the customer's review content.
    
    If any field is missing, use null. Return ONLY the JSON.
    """
    
    try:
        response = model.generate_content([prompt, image])
        # Clean up code blocks if present
        text_response = response.text.strip()
        
        # Try to find JSON block using regex
        match = re.search(r'\{.*\}', text_response, re.DOTALL)
        if match:
            json_str = match.group(0)
        else:
            # Fallback to original cleanup if no curly braces found (unlikely for valid JSON)
            json_str = text_response.replace('```json', '').replace('```', '').strip()
            
        data = json.loads(json_str)
        return data
    except Exception as e:
        return {"error": str(e)}

def analyze_sentiment_batch(reviews, language="English", stream=False):
    """
    Sends a batch of reviews to Gemini for sentiment analysis and recommendations.
    """
    configure_genai()
    # Using gemini-3-flash-preview as requested
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    reviews_text = json.dumps(reviews, indent=2)
    
    # Calculate Sentiment Stats (in Python to ensure accuracy)
    total_reviews = len(reviews)
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    
    for r in reviews:
        try:
            val = float(r.get('rating_overall', 0) or 0)
            
            # Sentiment bucket
            if val >= 4.5:
                sentiment_counts['Positive'] += 1
            elif val > 3.5:
                sentiment_counts['Neutral'] += 1
            else:
                sentiment_counts['Negative'] += 1
        except:
            pass

    stats_summary = f"""
    Total Reviews: {total_reviews}
    
    Sentiment Breakdown (3 Categories):
    - Positive (4.5 - 5.0): {sentiment_counts['Positive']} ({(sentiment_counts['Positive']/total_reviews)*100:.1f}%)
    - Neutral (4.0): {sentiment_counts['Neutral']} ({(sentiment_counts['Neutral']/total_reviews)*100:.1f}%)
    - Negative (<= 3.5): {sentiment_counts['Negative']} ({(sentiment_counts['Negative']/total_reviews)*100:.1f}%)
    """ if total_reviews > 0 else "No stats available."

    prompt = f"""
    You are a business intelligence analyst for a tea shop called "Southern Frontier".
    Analyze the following list of customer reviews and provide a summary report in {language}.
    
    Here are the pre-calculated statistics for this batch:
    {stats_summary}
    
    Reviews:
    {reviews_text}
    
    Provide a detailed intelligence report with the following structure:
    
    # 1. Sentiment Analysis
    - **Overall Summary**: High-level overview of customer sentiment.
    - **Sentiment Breakdown**: Present the 'Positive', 'Neutral', and 'Negative' stats provided above clearly. DO NOT create a 5-star breakdown.
    - **Polarity Analysis**: Summarize the KEY drivers for Positive vs. Neutral/Negative reviews. (Why are people happy vs. unhappy?)
    
    # 2. Customer Archetype Understanding
    - Based on the content and tone of the reviews, hypothesize 2-3 types of customer archetypes (e.g., "The Value Seeker", "The Tea Connoisseur", "The Aesthetic Lover").
    - **Recommendations**: For each archetype, provide specific recommendations on how to identify and target them better.
    
    # 3. Product Growth Recommendations
    - **Actionable Steps**: Provide a consolidated list of 3-5 high-impact recommendations covering product improvements, marketing angles, and operational changes to drive growth. Focus on what to *do* next.
    
    IMPORTANT:
    - Use the exact categories: 'Positive', 'Neutral', 'Negative' when translating (e.g. 正面, 中立, 负面 for Chinese).
    - Do NOT split into 5-star ratings.
    
    Format the output as Markdown.
    IMPORTANT: Do NOT include any "To", "From", "Date", or "Subject" lines at the top. 
    Start directly with the "# 1. Sentiment Analysis" or a title like "# Executive Summary".
    """
    
    try:
        response = model.generate_content(prompt, stream=stream)
        if stream:
            return response
        else:
            return response.text
    except Exception as e:
        return f"Error generating report: {str(e)}"

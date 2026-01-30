# 🍵 Southern Frontier Customer Review Intelligence

**Transforming customer feedback into business growth.**

This application is a comprehensive **Customer Review Intelligence System** built with **Streamlit**. It allows businesses to aggregate reviews from screenshots (using AI OCR), store them in a structured Postgres database, visualize trends, generate insights reports, and chat with their data using an AI assistant.

---

## ✨ Features

*   **📥 Review Ingestion via OCR**: Upload screenshots of customer reviews. The app uses **Google Gemini 3 Flash** to automatically extract:
    *   User Name
    *   Rating (Overall, Taste, Environment, Service, Value)
    *   Review Content
    *   Date
*   **🗄️ Centralized Database**: reliable storage using **Neon (Postgres)**.
*   **📈 Interactive Analytics**:
    *   Time-series trends for ratings and review volume.
    *   7-Day Rolling Averages.
    *   Sentiment Breakdown (Positive/Neutral/Negative).
*   **🤖 AI Intelligence**:
    *   **RAG Chatbot**: Chat with your review data ("What do customers say about our tea packaging?").
    *   **Automated Reports**: Generate and download PDF/DOCX/PPTX reports summarizing recent feedback.

---

## 🚀 Setup & Installation

### 1. Prerequisites
*   Python 3.9+
*   A **Supabase** or **Neon** Postgres database.
*   A **Google AI Studio** API Key.

### 2. Installation
Clone the repository and install dependencies:

```bash
git clone <your-repo-url>
cd Customer_Review_Intelligence
pip install -r requirements.txt
```

### 3. Configuration (Secrets)
This app utilizes `streamlit.secrets` for secure configuration.

1.  Create a file named `.streamlit/secrets.toml` in the project root.
2.  Add the following secrets:

    ```toml
    [general]
    debug = false

    # Database Connection (Neon/Postgres)
    # Format: postgres://user:password@endpoint.neon.tech/dbname?sslmode=require
    NEON_DB_CONNECTION_STRING = "your_postgres_connection_string_here"

    # Google Gemini API
    # Get yours at: https://aistudio.google.com/
    GOOGLE_API_KEY = "your_google_ai_studio_api_key_here"

    # Admin Access
    # Password to enable writing to the DB and uploading files
    ADMIN_PASSWORD = "your_secure_admin_password"
    ```

> **Note:** Do not commit `secrets.toml` to version control!

### 4. Running the App

```bash
streamlit run app.py
```

---

## 🧠 Original High-Level Prompt

This application was built using an **Agentic AI Workflow**. Below is the original high-level prompt that kickstarted the development process:


> **Mission: Build a Review Intelligence App**
>
> **Project Goal:** Create a full-stack web application that extracts structured data from uploaded screenshots of reviews, stores them in a database, and provides sentiment insights.
>
> **Core Features to Implement:**
>
> **Data Ingestion:** A frontend page to upload images. Use Gemini 3 Flash to process the images and extract: Username, Date, Total Rating, Rating Breakdown (Taste, Environment, Service, Value), and Review Content.
>
> **Database:** Set up a SQLite or PostgreSQL database. Create a schema to store the extracted data and ensure new uploads append to the existing table.
>
> **Dashboard:** A consolidated view showing a table of all reviews.
>
> **Analysis Engine:** A summary section that uses an LLM to analyze the entire database to provide:
> *   Overall sentiment (Positive/Neutral/Negative).
> *   Key recurring themes or complaints.
> *   Actionable suggestions for the business.
>
> **Tech Stack Preference:**
>
> *   **Frontend/Backend:** Python with Streamlit (for rapid prototyping) or FastAPI with a React frontend.
> *   **AI Integration:** Use the Gemini API for both OCR/Extraction and Sentiment Analysis.
>
> **Verification:** Once the code is written, use the integrated browser to test the upload flow with a sample image and verify the database entries appear in the dashboard.

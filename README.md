# 🍵 Southern Frontier Customer Review Intelligence

**Transforming customer feedback into business growth.**

This application is a comprehensive **Customer Review Intelligence System** built with **Streamlit**. It allows businesses to aggregate reviews from screenshots (using AI OCR), store them in a structured Postgres database, visualize trends, and chat with their data using an AI assistant.

---

## ✨ Features

*   **📥 Review Ingestion via OCR**: Upload screenshots of customer reviews (e.g., from food delivery apps). The app uses **Google Gemini Flash 1.5** to automatically extract:
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

> **"Build a specialized 'Customer Review Intelligence' dashboard for 'Southern Frontier' (a premium tea brand).**
>
> **Core Request:**
> I need a tool to aggregate and analyze customer reviews from screenshots. We have hundreds of reviews on delivery platforms but no API access.
>
> **Key Capabilities Needed:**
> 1.  **Ingestion**: A drag-and-drop web interface where I can upload screenshots of reviews. Use a Multimodal LLM (Gemini Flash) to 'read' these images and extract: Rating (Taste/Env/Service), Date, Content, and User Name.
> 2.  **Storage**: Save this structured data into a Postgres database (Neon) so we build a historical asset.
> 3.  **Visualization**: A 'Metrics' tab showing trends over time (moving averages of ratings), and volume of reviews.
> 4.  **AI Analyst**: I want to 'chat' with my data. Include a chatbot sidebar where I can ask 'Why did our service rating drop last week?' and it answers based on the actual review text.
> 5.  **Reporting**: A button to generate a 'Weekly Intelligence Report' as a PDF, summarizing sentiment and key actionable advice.
>
> **Tech Stack**: Streamlit (frontend), Python, Neon (DB), Google Gemini (AI)."

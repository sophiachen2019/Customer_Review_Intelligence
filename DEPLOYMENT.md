# Deploying Southern Frontier Review Intelligence to Streamlit Community Cloud

The easiest way to deploy this application is using **Streamlit Community Cloud**, which is free and connects directly to your GitHub repository.

## Prerequisites
1.  A **GitHub** account.
2.  A **Streamlit Community Cloud** account (sign up at [streamlit.io](https://streamlit.io/)).

## Step 1: Push Code to GitHub
Ensure all your files are committed and pushed to a GitHub repository.
1.  Initialize git (if not already done): `git init`
2.  Add files: `git add .`
3.  Commit: `git commit -m "Initial commit"`
4.  Create a new repo on GitHub.
5.  Link and push:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    git push -u origin main
    ```

## Step 2: Deploy on Streamlit Cloud
1.  Log in to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select your GitHub repository, branch (`main`), and the main file path (`app.py`).
4.  Click **"Deploy!"**.

## Step 3: Configure Secrets
The app will fail to start initially because it needs your API keys (Neon DB and Google Gemini).
1.  On your app's dashboard in Streamlit Cloud, click the **Settings** menu (three dots) -> **Settings** -> **Secrets**.
2.  Copy and paste your secrets in the TOML format below:

```toml
[general]
# Any general settings if needed

# Database Connection
NEON_DB_CONNECTION_STRING = "postgres://USER:PASSWORD@ep-example.region.aws.neon.tech/dbname?sslmode=require"

# Google Gemini API
GOOGLE_API_KEY = "your_google_ai_studio_api_key_here"
```

*Replace the values with your actual `NEON_DB_CONNECTION_STRING` and `GOOGLE_API_KEY` from your local `.env` or `secrets.toml` file.*

## Step 4: Verify
1.  Once secrets are saved, the app should automatically restart.
2.  Review the logs in the "Manage app" bottom right pane if any errors occur.
3.  Your app is now live! 🚀

## Troubleshooting
*   **ModuleNotFoundError**: Ensure `requirements.txt` is present in the root folder. I have updated it to include `fpdf`, `python-docx`, `psycopg2-binary`, etc.
*   **Database Error**: Ensure your Neon DB is accessible from "Anywhere" (0.0.0.0/0) or whitelisted for Streamlit Cloud (though Streamlit Cloud IPs vary, so "Anywhere" is easiest for development DBs).

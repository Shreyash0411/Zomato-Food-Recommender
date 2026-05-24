# AI-Powered Restaurant Recommendation System (Zomato)

An AI-powered restaurant recommendation service inspired by Zomato. It intelligently suggests restaurants based on user preferences by combining hard-filtering over structured Zomato data with a Large Language Model (Groq - Llama3).

## Features
- **Data Ingestion:** Automatically downloads and cleans the Zomato dataset from Hugging Face.
- **Smart Filtering Layer:** Instantly filters candidates based on strict Location, Budget, Cuisine, and Rating requirements.
- **AI Recommendations:** Feeds the top filtered candidates to the Groq LLM API to reason, select, and generate personalized explanations for the top 3 recommendations.
- **Interactive UI:** Built with Streamlit for a fast, responsive, modern frontend.

## Setup & Run Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   - Rename `.env.example` to `.env` (if not already done).
   - Ensure your Groq API Key is properly configured: `GROQ_API_KEY=gsk_...`

3. **Data Ingestion (First Run Only):**
   ```bash
   python src/data_ingestion.py
   ```
   *This downloads the Zomato dataset, cleans it, and creates `cleaned_zomato.csv` inside the `data/` folder.*

4. **Run the Streamlit Application:**
   ```bash
   streamlit run app.py
   ```
   *This will automatically open the UI in your default web browser.*

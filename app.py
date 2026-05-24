import streamlit as st
import pandas as pd
from src.backend import RestaurantFilter
from src.llm_engine import RecommendationEngine

# Page Config
st.set_page_config(page_title="Zomato AI Recommender", page_icon="🍔", layout="centered")

st.title("🍔 Zomato AI Restaurant Recommender")
st.markdown("Get personalized, AI-curated restaurant recommendations based on real Zomato data.")

# Initialize Backend and LLM Engine
@st.cache_resource
def load_backend():
    data_path = "data/cleaned_zomato.csv"
    try:
        return RestaurantFilter(data_path)
    except Exception as e:
        st.error(f"Failed to load dataset: {str(e)}")
        return None

@st.cache_resource
def load_llm():
    try:
        return RecommendationEngine()
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        return None

filter_engine = load_backend()
llm_engine = load_llm()

if filter_engine is None or filter_engine.df.empty or llm_engine is None:
    st.error("⚠️ Failed to load the dataset or LLM API. Please ensure `data/cleaned_zomato.csv` exists and API keys are set.")
    st.stop()

# Sidebar / Main Area Inputs
with st.form("preferences_form"):
    st.subheader("What are you craving?")
    
    # Get unique locations from the dataset for the auto-suggest dropdown
    unique_locations = sorted(filter_engine.df['location'].dropna().unique().tolist())
    unique_locations.insert(0, "") # Add empty default option
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox("Location (Type to search)", options=unique_locations, index=0)
        cuisine = st.text_input("Cuisine", placeholder="e.g., Chinese, Italian, North Indian")
    
    with col2:
        budget = st.selectbox("Budget for Two", options=["Any", "Low", "Medium", "High"])
        min_rating = st.slider("Minimum Rating", min_value=1.0, max_value=5.0, value=3.5, step=0.1)
        
    additional_prefs = st.text_area("Additional Preferences", placeholder="e.g., Family friendly, extremely spicy, open rooftop seating")
    
    submit_button = st.form_submit_button("Find Restaurants")

if submit_button:
    with st.spinner("🔍 Searching and generating AI recommendations..."):
        # Map budget
        budget_category = None
        if budget != "Any":
            budget_category = budget.lower()
            
        # Step 1: Filter
        filtered_df = filter_engine.filter_restaurants(
            location=location if location else None,
            budget_category=budget_category,
            cuisine=cuisine if cuisine else None,
            min_rating=min_rating,
            top_n=10
        )
        
        if filtered_df.empty:
            st.error("❌ No restaurants found matching those strict filters. Try lowering the rating or changing the location/budget.")
        else:
            # Step 2: Format for LLM
            filtered_json = filter_engine.format_for_llm(filtered_df)
            
            user_prefs = {
                "location": location,
                "budget": budget,
                "cuisine": cuisine,
                "min_rating": min_rating,
                "additional_preferences": additional_prefs
            }
            
            # Step 3: LLM Generation
            response = llm_engine.generate_recommendations(user_prefs, filtered_json)
            
            # Step 4: Display Results
            st.subheader("✨ Your AI Recommendations")
            if "Error generating" in response or "Error code:" in response:
                st.error(response)
            else:
                st.success("Successfully generated personalized recommendations!")
                st.markdown(response)
                
            with st.expander("🛠️ View Filtered Candidates (Behind the scenes)"):
                st.dataframe(filtered_df[['name', 'location', 'cuisines', 'rating', 'cost_for_two', 'votes']])

import os
import pandas as pd
from datasets import load_dataset
import re

def clean_rate(rate_str):
    if pd.isna(rate_str) or rate_str == 'NEW' or rate_str == '-':
        return None
    try:
        # rate comes as '4.1/5' or '4.1 /5', extract just the first part
        return float(rate_str.split('/')[0].strip())
    except:
        return None

def clean_cost(cost_str):
    if pd.isna(cost_str):
        return None
    try:
        # Cost comes as '1,200', remove comma and convert to int
        cost_str = str(cost_str).replace(',', '')
        return float(cost_str)
    except:
        return None

def main():
    print("Loading Zomato dataset from Hugging Face...")
    dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
    
    # Get the train split
    df = dataset['train'].to_pandas()
    print(f"Original Data Shape: {df.shape}")
    
    # Select relevant columns
    cols_to_keep = [
        'name', 
        'location', 
        'cuisines', 
        'approx_cost(for two people)', 
        'rate', 
        'votes'
    ]
    df = df[cols_to_keep]
    
    print("Cleaning Data...")
    # Drop rows where critical fields are missing
    df = df.dropna(subset=['name', 'location', 'cuisines'])
    
    # Clean rating and cost
    df['rating'] = df['rate'].apply(clean_rate)
    df['cost_for_two'] = df['approx_cost(for two people)'].apply(clean_cost)
    
    # Drop old uncleaned columns
    df = df.drop(columns=['rate', 'approx_cost(for two people)'])
    
    # Drop rows with missing rating or cost for simplicity in recommendation (optional, but good for Phase 1)
    df = df.dropna(subset=['rating', 'cost_for_two'])
    
    # Fill votes with 0 if missing and convert to int
    df['votes'] = df['votes'].fillna(0).astype(int)
    
    print(f"Cleaned Data Shape: {df.shape}")
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save the cleaned data
    output_path = 'data/cleaned_zomato.csv'
    df.to_csv(output_path, index=False)
    print(f"Cleaned data successfully saved to: {output_path}")

if __name__ == "__main__":
    main()

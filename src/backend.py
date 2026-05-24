import pandas as pd
import json

class RestaurantFilter:
    def __init__(self, data_path: str):
        """
        Step 2.1: Data Loading
        """
        try:
            self.df = pd.read_csv(data_path)
            # Create lowercase columns for robust string matching
            self.df['location_lower'] = self.df['location'].astype(str).str.lower()
            self.df['cuisines_lower'] = self.df['cuisines'].astype(str).str.lower()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.df = pd.DataFrame()

    def filter_restaurants(self, location: str = None, budget_category: str = None, 
                           cuisine: str = None, min_rating: float = None, top_n: int = 15):
        """
        Step 2.2: Hard Filtering Logic
        budget_category: 'low' (<500), 'medium' (500-1500), 'high' (>1500)
        """
        if self.df.empty:
            return pd.DataFrame()

        filtered_df = self.df.copy()

        if location:
            loc_lower = location.lower().strip()
            # Since the whole dataset is Bangalore, ignore generic city terms
            if loc_lower not in ['bangalore', 'bengaluru', 'blr', 'any']:
                filtered_df = filtered_df[filtered_df['location_lower'].str.contains(loc_lower, na=False)]
            
        if cuisine:
            filtered_df = filtered_df[filtered_df['cuisines_lower'].str.contains(cuisine.lower(), na=False)]
            
        if min_rating is not None:
            filtered_df = filtered_df[filtered_df['rating'] >= float(min_rating)]
            
        if budget_category:
            budget_category = budget_category.lower()
            if budget_category == 'low':
                filtered_df = filtered_df[filtered_df['cost_for_two'] < 500]
            elif budget_category == 'medium':
                filtered_df = filtered_df[(filtered_df['cost_for_two'] >= 500) & (filtered_df['cost_for_two'] <= 1500)]
            elif budget_category == 'high':
                filtered_df = filtered_df[filtered_df['cost_for_two'] > 1500]

        # Sort by rating and votes to surface the best options
        filtered_df = filtered_df.sort_values(by=['rating', 'votes'], ascending=[False, False])
        
        # Drop duplicate restaurants to ensure variety
        filtered_df = filtered_df.drop_duplicates(subset=['name'])
        
        # Limit to top N to avoid exceeding LLM context window sizes
        filtered_df = filtered_df.head(top_n)
        
        return filtered_df

    def format_for_llm(self, filtered_df: pd.DataFrame) -> str:
        """
        Step 2.3: Data Structuring
        Format the filtered candidates into a JSON string that can be injected into the LLM prompt.
        """
        if filtered_df.empty:
            return "No restaurants found matching the specified criteria."
            
        # Select original user-friendly columns for output
        cols_to_export = ['name', 'location', 'cuisines', 'rating', 'cost_for_two', 'votes']
        results = filtered_df[cols_to_export].to_dict(orient='records')
        
        return json.dumps(results, indent=2)

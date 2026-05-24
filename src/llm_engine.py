import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RecommendationEngine:
    def __init__(self):
        """
        Step 3.1: LLM Setup
        Initializes the Groq client.
        """
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables.")
        self.client = Groq(api_key=self.api_key)
        # Using an updated and supported model on Groq
        self.model = "llama-3.3-70b-versatile"

    def generate_recommendations(self, user_preferences: dict, filtered_restaurants_json: str) -> str:
        """
        Step 3.2 & 3.3: Prompt Design and Response parsing
        """
        prompt = f"""
You are an expert AI Restaurant Recommender based on Zomato data.
Your task is to analyze the user's specific preferences and a list of filtered restaurant candidates, then provide the top 5 recommendations.

User Preferences:
- Location: {user_preferences.get('location', 'Any')}
- Budget: {user_preferences.get('budget', 'Any')}
- Cuisine: {user_preferences.get('cuisine', 'Any')}
- Min Rating: {user_preferences.get('min_rating', 'Any')}
- Additional Preferences: {user_preferences.get('additional_preferences', 'None')}

Filtered Restaurant Candidates (in JSON format):
{filtered_restaurants_json}

Instructions:
1. Review the candidate restaurants.
2. Select the top 5 best matching restaurants based on rating, votes, and especially how well they align with the user's 'Additional Preferences'.
3. If there are fewer than 5 candidates, recommend all of them.
4. For each recommended restaurant, provide a short personalized explanation of why it's a good fit based on the user's preferences.

Output Format:
Respond STRICTLY in Markdown format as follows:

### 1. [Restaurant Name]
- **Cuisine:** [Cuisine]
- **Rating:** [Rating]
- **Cost for Two:** ₹[Cost]
- **Why we recommend it:** [Your personalized explanation]

### 2. [Restaurant Name]
...
"""
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful, enthusiastic, and expert food recommendation assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"

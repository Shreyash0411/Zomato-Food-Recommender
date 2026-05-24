import os
import unittest
from dotenv import load_dotenv
from src.llm_engine import RecommendationEngine

class TestLLMEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.engine = RecommendationEngine()
        
    def test_generation(self):
        # A simple fake list of candidates
        fake_json = '''
        [
          {"name": "Spice Elephant", "location": "Banashankari", "cuisines": "Chinese, North Indian, Thai", "rating": 4.1, "cost_for_two": 800.0, "votes": 787},
          {"name": "San Churro Cafe", "location": "Banashankari", "cuisines": "Cafe, Mexican, Italian", "rating": 3.8, "cost_for_two": 800.0, "votes": 918}
        ]
        '''
        
        user_prefs = {
            "location": "Banashankari",
            "budget": "medium",
            "cuisine": "Chinese",
            "min_rating": 4.0,
            "additional_preferences": "I want something spicy"
        }
        
        print("\n--- Sending request to Groq LLM ---")
        response = self.engine.generate_recommendations(user_prefs, fake_json)
        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 50)
        self.assertNotIn("Error generating", response)
        print("LLM Response:\n", response.encode('utf-8', 'replace').decode('utf-8'))
        print("-----------------------------------\n")

if __name__ == '__main__':
    unittest.main()

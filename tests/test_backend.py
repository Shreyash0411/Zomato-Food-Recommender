import unittest
import pandas as pd
import os
import tempfile
from src.backend import RestaurantFilter

class TestRestaurantFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create dummy data for testing
        cls.dummy_data = [
            {'name': 'Cheap Chinese', 'location': 'Delhi', 'cuisines': 'Chinese', 'rating': 3.5, 'cost_for_two': 300, 'votes': 100},
            {'name': 'Good Chinese', 'location': 'Delhi', 'cuisines': 'Chinese', 'rating': 4.5, 'cost_for_two': 800, 'votes': 500},
            {'name': 'Fancy Italian', 'location': 'Delhi', 'cuisines': 'Italian', 'rating': 4.8, 'cost_for_two': 2000, 'votes': 300},
            {'name': 'Bangalore Dosa', 'location': 'Bangalore', 'cuisines': 'South Indian', 'rating': 4.2, 'cost_for_two': 200, 'votes': 1000},
            {'name': 'Bad Dosa', 'location': 'Bangalore', 'cuisines': 'South Indian', 'rating': 2.5, 'cost_for_two': 100, 'votes': 10},
        ]
        cls.df = pd.DataFrame(cls.dummy_data)
        
        # Use a temporary file for testing
        cls.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        cls.test_path = cls.temp_file.name
        cls.df.to_csv(cls.test_path, index=False)
        cls.temp_file.close()
        
        cls.filter_engine = RestaurantFilter(cls.test_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_path):
            os.remove(cls.test_path)

    def test_filter_location(self):
        res = self.filter_engine.filter_restaurants(location='Bangalore')
        self.assertEqual(len(res), 2)
        self.assertTrue(all(res['location'] == 'Bangalore'))

    def test_filter_cuisine(self):
        res = self.filter_engine.filter_restaurants(cuisine='Chinese')
        self.assertEqual(len(res), 2)

    def test_filter_rating(self):
        res = self.filter_engine.filter_restaurants(min_rating=4.5)
        self.assertEqual(len(res), 2)

    def test_filter_budget(self):
        res_low = self.filter_engine.filter_restaurants(budget_category='low')
        self.assertEqual(len(res_low), 3) # 300, 200, 100
        
        res_high = self.filter_engine.filter_restaurants(budget_category='high')
        self.assertEqual(len(res_high), 1)
        self.assertEqual(res_high.iloc[0]['name'], 'Fancy Italian')

    def test_combined_filters(self):
        res = self.filter_engine.filter_restaurants(location='Delhi', cuisine='Chinese', min_rating=4.0)
        self.assertEqual(len(res), 1)
        self.assertEqual(res.iloc[0]['name'], 'Good Chinese')

    def test_format_for_llm(self):
        res = self.filter_engine.filter_restaurants(location='Delhi', cuisine='Chinese', min_rating=4.0)
        formatted = self.filter_engine.format_for_llm(res)
        self.assertIn('Good Chinese', formatted)
        self.assertIn('800', formatted)

if __name__ == '__main__':
    unittest.main()

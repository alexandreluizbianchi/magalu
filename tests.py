import unittest
import pandas as pd
import numpy as np
import util


# Leitura dos datasets:
train_data = pd.read_csv('challenge_train.csv')
test_data = pd.read_csv('challenge_test.csv')

train_data.drop('name', axis=1, inplace=True)
test_data.drop('name', axis=1, inplace=True)

# Um exemplo de teste...

class TestMethods(unittest.TestCase):
    def test_content(self):

        self.assertListEqual(            
            list(util.search_data_by_id(1118, train_data, test_data).values[0]), 
            [5, 0, 0, 'spell', 'nature']
        )
        
        self.assertListEqual(            
            list(util.search_data_by_id(100042, train_data, test_data).values[0]), 
            [1, 1, 1, 'creature', 'nature']
        )
        
        self.assertIsNone(            
            util.search_data_by_id(1928374, train_data, test_data)
        )
        
        self.assertListEqual(            
            list(util.search_data_by_id(1090, train_data, test_data).values[0]), 
            [6, 4, 8, 'creature', 'neutral']
        )
        
        self.assertListEqual(            
            list(util.search_data_by_id(244, train_data, test_data).values[0]), 
            [6, 4, 4, 'creature', 'neutral']
        )
        
        self.assertIsNone(            
            util.search_data_by_id(-2, train_data, test_data)
        )
        
        self.assertIsNone(            
            util.search_data_by_id(-1, train_data, test_data)
        )
    
if __name__ == '__main__':
    unittest.main()

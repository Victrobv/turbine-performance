# Unit tests
import unittest
from unittest.mock import patch
import pandas as pd
from excel_to_dict import excel2dict, dir2dict

class TestExcelToDict(unittest.TestCase):
    
    ### Test cases for excel2dict
            
    def test_create_df_dict_value_error(self):
        with patch('pandas.ExcelFile') as mock_file:
            mock_file.side_effect = ValueError
            
            with self.assertRaises(ValueError):
                excel2dict("mock_file.txt")
        
    def test_create_df_dict_corrupted_file_error(self):
        with patch('pandas.ExcelFile') as mock_corrupted_file:
            mock_corrupted_file.side_effect = pd.errors.ParserError
            
            with self.assertRaises(pd.errors.ParserError):
                excel2dict("mock_corrupted_file.xlsx")
        
    def test_create_df_dict_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            excel2dict("nonexistent_file.xlsx")
                

    ### Test cases for dir2dict                
        
    def test_create_dict_from_nonexistent_dir(self):
        with self.assertRaises(FileNotFoundError):
            dir2dict("nonexistent_dir")

if __name__ == "__main__":
  unittest.main()
  


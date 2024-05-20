# Unit tests
import unittest
import pandas as pd
import numpy as np
from multi_interp import MultiInterp

class InterpTest(unittest.TestCase):
  
  ### Data type tests
  
  def test_df_type_error(self):
    # Test for non DataFrame/Series input data
    df = "This is not a DataFrame"
    x = np.array([1, 2, 3])
    with self.assertRaises(ValueError):
      MultiInterp(df, x)
  
  def test_x_dim_1D_type_error(self):
    # Test for non 1D x for Series input data
    x = np.array([[1.5, 2.5], ])
    df = pd.Series([1, 2, 3], index=[1.0, 2.0, 3.0])
    with self.assertRaises(ValueError):
      MultiInterp(pd.Series(df, x))
      
  def test_x_dim__2D_type_error(self):
    # Test for non 2D x for DataFrame input data
    x = np.array([[1.5, 2.5, 3.5], ])
    df = pd.DataFrame([[1, 2], [3, 4]], index=[1.0, 2.0], columns=[3.0, 4.0])
    with self.assertRaises(ValueError):
      MultiInterp(pd.Series(df, x))
      
  ### Functionality tests 
    
  def test_1d_interpolation(self):
    # Create 1D data as pandas Series
    df = pd.Series([10, 20, 30, 40], index=[0, 1, 2, 3])
    x = np.array([1.5])
    result = MultiInterp(df, x)
    self.assertTrue(np.isreal(result))

  def test_2d_interpolation(self):
    # Create 2D data as pandas DataFrame
    df = pd.DataFrame([[1, 2], [1.5, 3]], index=[1.0, 2.0], columns=[10, 20])
    x = np.array([[1.2, 18]], )  # Points for interpolation
    result = MultiInterp(df, x)
    self.assertTrue(np.isreal(result))
    
if __name__ == "__main__":
  unittest.main()
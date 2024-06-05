import numpy as np
import pandas as pd
from interpolation import MultiInterp

def ComputeCoeffs(tables_dict, x):
    """
    Description.

    Args:
        tables_dict (dict): A dictionary containing multiple dictionaries of tables. 
        Each inner dictionary is assumed to have table names (strings) as keys and DataFrames (from pandas) as values.
        x (DataFrame): An ambient data DataFrame containing data used for interpolation. 

    Returns:
        dict: dict containing the interpolation results for all the tables as values, and coefficient index as keys.
    """  
    coeffs_dict = {'A': 1, 'B' : 1, 'C' : 1, 'D' : 0, 'E' : 1}
    
    # For every dict of tables in the main dict
    for _, table_dict in tables_dict.items():
        
        # For every table in a dict
        for name, table in table_dict.items():
            
            prefix = name[:-1] # Table Name
            index = name[-1]   # Coeff Index
        
            if name.startswith('T'): 
                coeff = MultiInterp(table, x['T'].values)
                continue
            else:
                coeff = MultiInterp(table, x[[prefix, 'T']].values)
                
            if index == 'D':
                coeffs_dict[index] += coeff
            else:
                coeffs_dict[index] *= coeff

    return coeffs_dict

def BaseLoad(coeffs_dict, ambient_df):
    """
    Description.

    Args:
        coeffs_dict (dict): A dictionary containing the interpolation results for all the tables as values, 
        and coefficient index as keys. (Output of ComputeCoeffs)
        ambient_df (DataFrame): An ambient data DataFrame containing data used for interpolation. .

    Returns:
        df: A DataFrame containing the calculated performance parameters based on ambient conditions and interpolation coefficients.
    """    
    # Simple Cycle DataSheet for GE 7E.03 EA
    OUT = 90_000     #kW 
    HR = 10_664      #kJ/kWh (LHV)
    HC = OUT * HR    #kW
    TX = 1010        #F
    EF = 1_079_000   #kg/h
    
    GE = {
        "A":OUT,
        "B":HR,
        "C":HC,
        "D":TX,
        "E":EF
    }
    
    perf_map = {
        "A":"Output",
        "B":"Heat Rate",
        "C":"Heat Consumption",
        "D":"Exhaust Temperature",
        "E":"Exhaust Flow"
    }
    
    performance_df = pd.DataFrame(index=ambient_df.index)
        
    for i, v in coeffs_dict.items():
        if i == "D":
            performance_df[perf_map[i]] = GE[i] + v
        else:
            performance_df[perf_map[i]] = GE[i] * v       
    
    return performance_df
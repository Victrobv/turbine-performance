import pandas as pd
from interpolation import MultiInterp

def ComputeCoeffs(nested_df_dict, x):
    """
    Description.
    Args:
        nested_df_dict (dict): A nested dictionary containing multiple dictionaries of tables. 
        Each inner dictionary is assumed to have table names (strings) as keys and DataFrames (from pandas) as values.
        x (DataFrame): An ambient data DataFrame containing data used for interpolation. 

    Returns:
        coeffs_dict: dict containing the interpolation results for all the tables as values, and coefficient index as keys.
    """  
    coeffs_dict = {"A": 1, "B" : 1, "C" : 1, "D" : 0, "E" : 1}
    
    # For every dict of tables in the main dict
    for _, df_dict in nested_df_dict.items():
        
        # For every table in a dict
        for name, df in df_dict.items():
            
            pref = name[:-1] # Table Name
            idx = name[-1]   # Coeff Index
        
            if name.startswith("T"):
                coeff = MultiInterp(df, x["T"].values)
                continue
            else:
                coeff = MultiInterp(df, x[[pref, "T"]].values)
                
            if idx == "D":
                coeffs_dict[idx] += coeff
            else:
                coeffs_dict[idx] *= coeff

    return coeffs_dict

# ------------------------------------------- #

def BaseLoad(nested_df_dict, ambient_df):
    """
    Description.

    Args:
        nested_df_dict (dict): A nested dictionary containing multiple dictionaries of tables. 
        Each inner dictionary is assumed to have table names (strings) as keys and DataFrames (from pandas) as values.
        ambient_df (DataFrame): An ambient data DataFrame containing data used for interpolation. .

    Returns:
        performance_df: A DataFrame containing the calculated performance parameters based on ambient conditions and interpolation coefficients.
    """    
    # Simple Cycle DataSheet for GE 7E.03 EA
    OUT = 90_000     #kW 
    HR = 10_664      #kJ/kWh (LHV)
    HC = OUT * HR    #kW
    TX = 1010        #F
    EF = 1_079_000   #kg/h
    
    value_map = {
        "A":OUT,
        "B":HR,
        "C":HC,
        "D":TX,
        "E":EF
    }
    
    name_map = {
        "A":"Output",
        "B":"Heat Rate",
        "C":"Heat Consumption",
        "D":"Exhaust Temperature",
        "E":"Exhaust Flow"
    }
    
    coeffs_dict = ComputeCoeffs(nested_df_dict, ambient_df)
    
    performance_df = pd.DataFrame(index=ambient_df.index)
        
    for idx, val in coeffs_dict.items():
        if idx == "D":
            performance_df[name_map[idx]] = value_map[idx] + val
        else:
            performance_df[name_map[idx]] = value_map[idx] * val       
    
    return performance_df

# ------------------------------------------- #

def PartLoad(data_tables_df_dict, partial_load_dict, ambient_df):
    """
    Description.

    Args:
        data_tables_df (dict): A nested dictionary containing multiple dictionaries of performance characteristics tables. 
        Each inner dictionary is assumed to have table names (strings) as keys and DataFrames (from pandas) as values.
        partial_load_dict (dict): A nested dictionary containing a single dictionary of DataFrames for partial load tables.
        ambient_df (DataFrame): An ambient data DataFrame containing data used for interpolation.

    Returns:
        performance_S: A DataFrame containing the calculated sample performance based on ambient conditions and interpolation coefficients.
    """  
    ambient_df_O = ambient_df.copy()

    temp_O    = 59.0
    rel_hum_O = 60.0

    ambient_df_O["T"] = temp_O
    ambient_df_O["RH"] = rel_hum_O
    
    performance_O = BaseLoad(data_tables_df_dict, ambient_df_O)
    
    tables_O = {"T":data_tables_df_dict["T"], "RH":data_tables_df_dict["RH"]}
    
    ambient_df_O["PartLoad"] = ambient_df_O["PartLoad"] * ComputeCoeffs(tables_O, ambient_df_O)["A"]
    
    partial_load_coeffs = ComputeCoeffs(partial_load_dict, ambient_df_O[["PartLoad", "T"]])
    
    perf_map = {
        "A":"Output",
        "B":"Heat Rate",
        "C":"Heat Consumption",
        "D":"Exhaust Temperature",
        "E":"Exhaust Flow"
    }
    
    performance_S = performance_O.copy()
    
    for index, coeff in partial_load_coeffs.items():
        if index == "D":
            performance_S[perf_map[index]] += coeff
        else:
            performance_S[perf_map[index]] *= coeff
    return performance_S
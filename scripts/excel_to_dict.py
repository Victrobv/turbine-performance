import pandas as pd
import os

def excel2dict(file_path):
    """
    Creates a dictionary of DataFrames from Excel sheets in a given file.

    Args:
        excel_file_path (str): Path to the .xlsx file.

    Returns:
        dict: Dictionary where keys are sheet names and values are DataFrames.
    """ 
  
    try:
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        data_dict = {}
        for sheet_name in sheet_names:
            data_dict[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name, index_col=0)
        return data_dict
    
    except (ValueError, FileNotFoundError, pd.errors.ParserError) as error:
        print(f"Error: {error}")
        raise

def dir2dict(dir_path):
    """
    Creates a dictionary of DataFrames from Excel sheets in a given directory.

    Args:
        dir_path (str): Path to the directory containing .xlsx files.

    Returns:
        dict: Dictionary where keys are file names and values are dictionaries of DataFrames.
    """ 
    dir_data_dict = {}
    
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory path does not exist. {dir_path}")
     
    for file_name in os.listdir(dir_path):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(dir_path, file_name)
            dir_data_dict[file_name.split(".")[0]] = excel2dict(file_path)
            
    if dir_data_dict == {}:
        raise ValueError("No .xlsx files found in the directory.")

    return dir_data_dict

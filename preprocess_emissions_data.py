"""
Loads each emissions csv and pre-processes it, ready for visualisation.
Ultimately, only the 'Total GHG' csv is needed.
"""
import utils as u
import pandas as pd

# Variables
PATH = 'Datasets/industry_emissions'
FILES = ['CH4', 'CO2', 'HFC', 'N2O', 'NF3', 'PFC', 'SF6', 'Total GHG']
DROP_COLS = ['Unnamed: 0']

# Specialised functions
def separate_detail(df: pd.DataFrame) -> pd.DataFrame:
    """
    Splits high-level and low-level breakdowns of emissions
    """
    base_df = df.iloc[:21, :]
    detail_df = df.iloc[21:,:]
    return base_df, detail_df

# Main logic
def run_process():
    # Create lists for storing each each CSV's data in a pandas DataFrame
    df_list = []  # For high-level industry overview
    df_detail_list = []  # For break-down of individual industries

    for emission in FILES:
        FILEPATH = PATH + '/' + emission + '.csv'
        # read data and remove unwanted cols
        data = pd.read_csv(FILEPATH)
        data = u.remove_cols(data, DROP_COLS)
        # split data and process separately
        base, detail = separate_detail(data)
        base, detail = base.T, detail.T
        base, detail = u.process_col_header(base), u.process_col_header(detail)
        df_list.append(base)
        df_detail_list.append(detail)
    
    return df_list, df_detail_list

if __name__ == '__main__':
    run_process()
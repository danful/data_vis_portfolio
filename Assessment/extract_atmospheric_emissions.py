"""
Emissions data contains several sheets - one for each of the main greenhouse gases, and a summary.
Each sheet is extracted into its own csv. Only the 'Total' GHG sheet is needed but rest might be 
useful/interesting.
"""
from preprocess_fossil_data import DROP_COLS
import utils as u
import pandas as pd
import os

# Define key variables
EXCEL_PATH = 'Datasets/atmosphericemissionsghg.xlsx'
SHEETS = ['Total GHG', 'CO2', 'CH4', 'N2O', 'HFC', 'PFC', 'NF3', 'SF6']
DROP_ROWS = [0, 1, 2, 25, 26, 27, 28, 29, 30, 31, 163, 164, 165, 166, 167, 168, 169]
NEW_COLS = [(0, 'Section'), (2, 'Section Description')]
DROP_COLS = ['Section']
EMISSIONS_PATH = 'Datasets/industry_emissions'


# Define any specialised functions
def replace_sic_with_section(df: pd.DataFrame) -> pd.DataFrame():
    df.iloc[23:,0] = df.iloc[23:,1]
    df.drop(df.columns[1], axis=1, inplace=True)

    return df


def create_section_lookup(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a dataframe with section and corresponding section description.
    Very helpful for breaking down section emissions further.
    """
    lookup_df = df[['Section', 'Section Description']]

    return lookup_df

# Run script logic
def run_process():
    data_dict = u.load_excel(EXCEL_PATH, SHEETS)  # load excel document
    data_dict = u.remove_rows(data_dict, DROP_ROWS)  # Removes unwanted rows from all sheets
    
    for key in data_dict.keys():
        # for each sheet (key) in document...
        data_dict[key] = u.process_col_header(data_dict[key], NEW_COLS)
        data_dict[key] = replace_sic_with_section(data_dict[key])  # renaming and reformat
        if key == 'Total GHG':
            data_dict[key] = data_dict[key].iloc[:-2,:]  # Really not sure why this only applies to this one
            lookup_df = create_section_lookup(data_dict[key]) # only needs to be done once as values same for all DFs
        data_dict[key] = u.remove_cols(data_dict[key], DROP_COLS)
        
        
    # Write to csv
    os.makedirs(EMISSIONS_PATH, exist_ok=True)
    for key in data_dict.keys():
        df = data_dict[key]
        df.to_csv(f'{EMISSIONS_PATH}/{key}.csv')
    lookup_df.to_csv(f'{EMISSIONS_PATH}/section_lookup.csv')


if __name__ == '__main__':
    run_process()


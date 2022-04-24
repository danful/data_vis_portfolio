from xml.dom.minidom import Element
from xml.sax import default_parser_list
from extract_atmospheric_emissions import NEW_COLS
import utils as u
import pandas as pd

# Define key variables
EXCEL_PATH = 'Datasets/renewablesources_manualextract.xlsx'  # original file was .xls, and wouldn't load
SHEETS = 'Sheet1'

# Define any specialised functions

# Run script logic
# Format data from top -> bottom
def run_process():
    df = u.load_excel(EXCEL_PATH, SHEETS)
    
    # process columns (decimal -> years)
    NEW_COLS = []
    for idx, col in enumerate(df.iloc[0,1:]):
        col = int(col)
        element = (idx+1, col)
        NEW_COLS.append(element)
    df = u.process_col_header(df, NEW_COLS)
    df.to_csv('Datasets/energy_from_renewables.csv')

if __name__ == '__main__':
    run_process()


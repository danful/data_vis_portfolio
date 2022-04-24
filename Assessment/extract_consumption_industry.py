from xml.sax import default_parser_list
import utils as u
import pandas as pd

# Define key variables
EXCEL_PATH = 'Datasets/energyconsumptionbyindustry.xlsx'
SHEETS = ['Energy consumption (Mtoe)', 'Energy consumption (PJ)']
DROP_ROWS = [0, 1, 2, 4, 5, 6, 7]
NEW_COLS = [(0, 'Industry')]

# Define any specialised functions


# Run script logic
# Format data from top -> bottom
def run_process():
    data_dict = u.load_excel(EXCEL_PATH, SHEETS)
    data_dict = u.remove_rows(data_dict, DROP_ROWS)
    
    for key in data_dict.keys():
        data_dict[key] = u.process_col_header(data_dict[key], NEW_COLS)
        data_dict[key] = data_dict[key].iloc[:21,:]  # Remove tail
    
    df = data_dict['Energy consumption (Mtoe)']
    df.to_csv('Datasets/energy_from_fossil.csv')
    

if __name__ == '__main__':
    run_process()


"""
Pre-process fossil fuel consumption data which was extracted from excel document.
"""
import utils as u
import pandas as pd

# Variables
FILEPATH = 'Datasets/energy_from_fossil.csv'
DROP_COLS = ['Unnamed: 0']

# Main logic
def run_process():
    data = pd.read_csv(FILEPATH)
    data = u.remove_cols(data, DROP_COLS)
    data = data.T  # year from index -> column headers
    data = u.process_col_header(data)
    data = data.replace('"', '')  # cleaning data

    return data

if __name__ == '__main__':
    run_process()
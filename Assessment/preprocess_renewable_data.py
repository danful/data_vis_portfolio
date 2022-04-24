import utils as u
import pandas as pd

# Variables
FILEPATH = 'Datasets/energy_from_renewables.csv'
DROP_COLS = ['Unnamed: 0']

# Specialised functions

# Main logic
def run_process():
    data = pd.read_csv(FILEPATH)
    data = u.remove_cols(data, DROP_COLS)
    data = data.T
    data = u.process_col_header(data)
    data = data.replace('"', '')

    return data

if __name__ == '__main__':
    run_process()
"""
Python file for storing functions which are used in multiple scripts.
"""

from typing import Type
import pandas as pd
import numpy as np

def load_excel(filepath: str, sheet_names: list) -> dict:
    """
    Loads data from excel file into dictionary of dataframes.
    Each df will have key corresponding to sheet name
    """
    if 'Contents' in sheet_names:
        sheet_names.remove('Contents')

    df_dict = pd.read_excel(io=filepath, sheet_name=sheet_names, header = None)
    return df_dict

def remove_rows(df_dict: dict, row_list: list) -> pd.DataFrame:
    """
    Drop set of rows for all dataframes in dataframe dict.
    Only works if wanting to drop same rows in all dataframes of dict.
    """
    for key in df_dict:
        df = df_dict[key]
        df = df.drop(row_list)
        df.reset_index(drop = True, inplace = True)
        df_dict[key] = df

    return df_dict

def remove_cols(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    If column from cols in datafram, drop it.
    """
    df = df.copy()
    for col in cols:
        if col in df.columns:
            df.drop(columns=col, inplace=True)

    return df

def create_new_header(existing_header:list, rename_list:list) -> list:
    """
    Create header for dataframe.
    rename_list should have format: [(idx0, new_name), ..., (idxn, new_name)].
    """
    new_header = existing_header

    for item in rename_list:
        idx, new_name = item[0], item[1]
        new_header[idx] = new_name
    
    for i, col in enumerate(new_header):
        try:
            new_header[i] = int(col)
        except:
            continue

    return new_header


def process_col_header(df: pd.DataFrame, rename_list: list = None) -> pd.DataFrame:
    """
    Creates new header for dataframe. Assumes that top row is meant to be header.
    """
    header = df.iloc[0].values
    if rename_list:
        header = create_new_header(header, rename_list)
    df.columns = header
    df = df[1:]  # Remove top row (now header)
    return df

def transform_data(df: pd.DataFrame, sort_year: str) -> pd.DataFrame:
    """
    Transform and reduce size of dataframe to reduce clutter in visualisation
    """
    n_years = len(df.index)
    df = df.T.sort_values(sort_year, ascending=True)
    df_top = df.iloc[-5:]
    df_other = df.iloc[:-5].sum().values
    df_other = pd.DataFrame(df_other.reshape(1,n_years), columns=df_top.columns, index = ['Other'])
    df_vis = df_other.append(df_top)
    
    return df_vis


def annotate_plot(vis_df: pd.DataFrame, ax, colours, labels, options = list):
    """
    Annotate a given plot based on data from vis_df. Requires:
    - vis_df to pull annotation values
    - ax to plot text on
    - colours to fill text boxes
    - labels to use replace headers which are too long
    - options which select which labels are shown
    """
    cols = vis_df.columns
    first_year = cols[0]
    last_year = cols[-1]
    middle_year = cols[len(cols)//2]

    for year in [first_year, last_year]:
        if year == first_year:
            sign = '-'
        else:
            sign = ''
        total = round(vis_df.sum()[year],1)
        ax.text(x = int(year) - 1990, y = total + 0.01*total, s = total, rotation = 45)
        ax.annotate("",
            xy = (int(year) - 1990, total), xycoords = 'data',
            xytext = (int(year) - 1990, 0), textcoords = 'data',
            arrowprops = dict(arrowstyle = '-', connectionstyle = f'bar,fraction={sign}0.03')
        )

    for idx, industry in enumerate(vis_df.index):
        val_0 = round(vis_df.loc[industry][first_year],1)
        val_1 = round(vis_df.loc[industry][last_year],1)
        val_mid = round(vis_df.loc[industry][middle_year],1)

        y0 = vis_df.cumsum(axis=0).loc[industry][first_year] - (val_0/1.8)
        y1 = vis_df.cumsum(axis=0).loc[industry][last_year] - (val_1/1.8)
        y_mid = vis_df.cumsum(axis=0).loc[industry][middle_year] - (val_mid/1.8)

        if options[0] == 1:
            ax.text(x = 0, y = y0, s = val_0, ha = 'center', bbox = dict(boxstyle = 'round', ec = '#cccccc',fc = 'w', alpha = 0.8))
        if options[1] == 1:
            ax.text(x = len(cols)//2, y = y_mid, s = labels[idx], ha = 'center', color = 'w')
        if options[2] == 1:
            ax.text(x = len(cols)-1, y = y1, s = val_1, ha = 'center', bbox = dict(boxstyle = 'round', ec= '#cccccc', fc = 'w', alpha = 0.8))


def format_axes(
    ax,
    remove_xticks:bool = True,
    remove_yticks:bool = True,
    remove_spines:list = []
    ) -> None:
    """
    Removes all but x-axis
    """
    if remove_xticks:
        ax.get_xaxis().set_visible(False)
    if remove_yticks:
        ax.get_yaxis().set_visible(False)
    for spine in remove_spines:
        ax.spines[spine].set_visible(False)


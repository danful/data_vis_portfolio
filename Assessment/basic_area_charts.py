import preprocess_emissions_data as emissions
import preprocess_fossil_data as fossil
import preprocess_renewable_data as renewable
import utils as u
# Import libraries required for visualisation and any additional formatting
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from conf import RENAME_DICT, DROP_COLS, COLOUR_DICT


## Variables

## Functions


## Load data
emissions_list, emissions_detail_list = emissions.run_process()
ghg_df = emissions_list[-1]  # Unit Kilotonnes of CO2 equivalent
fossil_df = fossil.run_process()  # Unit: Mtoe (Megatonnes of oil equivalent)
renewable_df = renewable.run_process()  # Unit: Mtoe

## Transform data
ghg_df = ghg_df.rename(columns = RENAME_DICT)
ghg_df = ghg_df.drop(columns = DROP_COLS)
fossil_df = fossil_df.rename(columns = RENAME_DICT)
fossil_df = fossil_df.drop(columns = DROP_COLS)
renewable_df = renewable_df.rename(columns = RENAME_DICT)
renewable_df = renewable_df.drop(columns = DROP_COLS)

ghg_vis_df = u.transform_data(ghg_df, '2020')
fossil_vis_df= u.transform_data(fossil_df, '2019')
renewable_vis_df= u.transform_data(renewable_df, '2019')

## GHG Plot
years = ghg_vis_df.columns
labels = list(ghg_vis_df.index)
colours = [COLOUR_DICT.get(label) for label in labels]

fig, ax = plt.subplots(figsize = (9,6.7))
ax.set_title('Greenhouse Gas Emissions by Industry Over Time\n($\mathregular{CO_2}$ Equivalent/Kilotonnes)')
ax.stackplot(years, ghg_vis_df.values.tolist(), colors=colours)
ax.legend(loc = 'upper right', labels = labels)
ax.set_xticklabels(years, rotation = 45)
u.format_axes(ax, remove_xticks=False, remove_yticks=False)
plt.show()

## Fossil fuel plot
years = fossil_vis_df.columns
labels = list(fossil_vis_df.index)
colours = [COLOUR_DICT.get(label) for label in labels]

fig, ax = plt.subplots(figsize = (9,6.7))
ax.set_title('Fossil fuel consumption by Industry (MTOE)')
ax.stackplot(years, fossil_vis_df.values.tolist(), colors=colours)
ax.set_xticklabels(years, rotation = 45)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
ax.legend(loc = 'upper right', labels = labels, bbox_to_anchor=(1.2, 1))
u.format_axes(ax, remove_xticks=False, remove_yticks=False)
plt.show()

## Renewable fuel plot
years = renewable_vis_df.columns
labels = list(renewable_vis_df.index)
colours = [COLOUR_DICT.get(label) for label in labels]

fig, ax = plt.subplots(figsize = (9,6.7))
ax.set_title('Renewable energy consumption by Industry (MTOE)')
ax.stackplot(years, renewable_vis_df.values.tolist(), colors=colours)
ax.set_xticklabels(years, rotation = 45)
ax.legend(loc = 'upper left', labels = labels)
u.format_axes(ax, remove_xticks=False, remove_yticks=False)
plt.show()

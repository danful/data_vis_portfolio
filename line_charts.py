# Import data pre-processing pipelines
from pyparsing import col
import preprocess_emissions_data as emissions
import preprocess_fossil_data as fossil
import preprocess_renewable_data as renewable
# Import libraries required for visualisation and any additional formatting
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from conf import RENAME_DICT, DROP_COLS, COLOUR_DICT

# Load data
emissions_list, emissions_detail_list = emissions.run_process()
ghg_df = emissions_list[-1]  # Unit Kilotonnes of CO2 equivalent
fossil_df = fossil.run_process()  # Unit: Mtoe (Megatonnes of oil equivalent)
renewable_df = renewable.run_process()  # Unit: Mtoe

# Transform data
ghg_df = ghg_df.rename(columns = RENAME_DICT)
ghg_df = ghg_df.drop(columns = DROP_COLS)
fossil_df = fossil_df.rename(columns = RENAME_DICT)
fossil_df = fossil_df.drop(columns = DROP_COLS)
renewable_df = renewable_df.rename(columns = RENAME_DICT)
renewable_df = renewable_df.drop(columns = DROP_COLS)

# Summarising total x over time
ghg_vis_df = ghg_df.sum(axis = 1)
y_ghg = ghg_vis_df.values
x_ghg = ghg_vis_df.index.values

fossil_vis_df = fossil_df.sum(axis=1)
y_foss = fossil_vis_df.values
x_foss = fossil_vis_df.index.values

renewable_vis_df = renewable_df.sum(axis=1)
y_ren = renewable_vis_df.values
x_ren = renewable_vis_df.index.values

# Emissions
fig, ax = plt.subplots(figsize = (9,7))
ax.plot(x_ghg, y_ghg, color = 'k')
ax.axvline(19, color = 'r', ls = '--')
ax.axvline(30, color = 'r', ls = '--')
ax.set_title('Total Greenhouse Gas Emissions by Year')
ax.text(18.7, 650000, 'Worst point of UK recession\nfollowing financial crisis', ha='right')
ax.text(29.7, 500000, 'COVID-19 Pandemic', ha='right')
ax.set_xlabel('Year')
ax.set_ylabel('CO2 Equivalent (Kilotonnes)')
ax.set_xticklabels(x_ghg, rotation = 45)
plt.show()

# Consumption
fig, ax = plt.subplots(figsize = (9,7))
ax.plot(x_foss, y_foss, color = 'k', label = 'From fossil fuels')
ax.plot(x_ren, y_ren, color = '#33a02c', label = 'From renewable sources')
ax.legend()
ax.set_title('Total Energy Consumption by Year')
ax.set_xlabel('Year')
ax.set_ylabel('Oil equivalent (Megatonnes)')
ax.set_xticklabels(x_foss, rotation = 45)
plt.show()


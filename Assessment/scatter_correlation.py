import preprocess_emissions_data as emissions
import preprocess_fossil_data as fossil
import preprocess_renewable_data as renewable
import utils as u
import scipy.stats as stats
# Import libraries required for visualisation and any additional formatting
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from conf import RENAME_DICT, DROP_COLS, COLOUR_DICT

## Variables

## Load data
emissions_list, emissions_detail_list = emissions.run_process()
ghg_df = emissions_list[-1]  # Unit Kilotonnes of CO2 equivalent
fossil_df = fossil.run_process()  # Unit: Mtoe (Megatonnes of oil equivalent)
renewable_df = renewable.run_process()  # Unit: Mtoe

## Transform data
ghg_df = ghg_df.drop('2020')
ghg_df = ghg_df.rename(columns = RENAME_DICT)
ghg_df = ghg_df.drop(columns = DROP_COLS)
ghg_df = ghg_df.reset_index()
ghg_df = pd.melt(ghg_df, id_vars = 'index', value_vars=ghg_df.columns, var_name='industry', value_name='emissions')

fossil_df = fossil_df.reset_index()
fossil_df = fossil_df.rename(columns = RENAME_DICT)
fossil_df = fossil_df.drop(columns = DROP_COLS)
fossil_df = pd.melt(fossil_df, id_vars = 'index', value_vars=fossil_df.columns, var_name='industry', value_name='consumption')

plot_df = pd.merge(ghg_df,fossil_df,how='inner', on=['index', 'industry'])

## Calculate correlation
corr = round(stats.pearsonr(plot_df['consumption'], plot_df['emissions'])[0],3)

## Plotting
# Coloured according to industry
fig, ax = plt.subplots(figsize = (12,7))
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
sns.scatterplot('consumption', 'emissions', data=plot_df, hue='industry', ax = ax, legend=True)
ax.set_xlabel('Fossil Fuel Consumption (Oil equivalent/Megatonnes)', fontsize = 13)
ax.set_ylabel('Total Greenhouse Gas Emissions\n($\mathregular{CO_2}$ Equivalent/Kilotonnes)', fontsize = 13)
ax.set_title('Fossil Fuel Consumption vs. Greenhouse Gas Emissions', fontsize = 14)
ax.legend(bbox_to_anchor=(1.01, 1))
ax.text(x=35, y=50000, s=f'Correlation: {corr}', fontsize = 14, fontweight ='bold')
plt.show()

# Not industry separation
fig, ax = plt.subplots(figsize = (9,7))
box = ax.get_position()
sns.scatterplot('consumption', 'emissions', data=plot_df, color = '#33a02c', ax = ax, legend=False)
ax.set_xlabel('Fossil Fuel Consumption (Oil equivalent/Megatonnes)', fontsize = 13)
ax.set_ylabel('Total Greenhouse Gas Emissions\n($\mathregular{CO_2}$ Equivalent/Kilotonnes)', fontsize = 13)
ax.set_title('Fossil Fuel Consumption vs. Greenhouse Gas Emissions', fontsize = 14)
ax.text(x=35, y=50000, s=f'Correlation: {corr}', fontsize = 14, fontweight ='bold')
plt.show()


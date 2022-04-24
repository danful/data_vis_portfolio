# Import data pre-processing pipelines
import preprocess_emissions_data as emissions
import preprocess_fossil_data as fossil
import preprocess_renewable_data as renewable
# Import libraries required for visualisation and any additional formatting
import utils as u
import pandas as pd
import numpy as np
import seaborn as sns
import squarify
from matplotlib import pyplot as plt
from conf import RENAME_DICT, DROP_COLS, COLOUR_DICT

## Variables

## Load data
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

## Selecting relevant data (most recent year's values)
ghg_plot_data = ghg_df.iloc[-1].sort_values(ascending = False)
fossil_plot_data = fossil_df.iloc[-1].sort_values(ascending = False)
renewable_plot_data = renewable_df.iloc[-1].sort_values(ascending = False)

## Plotting greenhouse gas treemap
# keep top five, roll rest up into 'other' to avoid clutter
sizes = list(ghg_plot_data.values)
sizes = sizes[:5] + [sum(sizes[5:])]
labels = list(ghg_plot_data.index)
labels = labels[:5] + ['Other']
colors = [COLOUR_DICT.get(label) for label in labels]
labels = [f'{label}: {round(sizes[i]/1000, 2)}K' if len(label) < 20 
else f'{label}:\n{round(sizes[i]/1000, 2)}K' for i, label in enumerate(labels)]
vert_label = labels[4]
labels[4] = ''

fig, ax = plt.subplots(figsize = (7.5,6))
squarify.plot(sizes=sizes, ax=ax, alpha = 0.85, color=colors, label = labels)
ax.set_title('Greenhouse Gas Emissions by Industry - 2020\n($\mathregular{CO_2}$ Equivalent/Kilotonnes)')
ax.text(51,56,vert_label,rotation=90)
u.format_axes(ax)
plt.show()

## Fossil Fuel Consumption
# keep top five, roll rest up into 'other' to avoid clutter
sizes = list(fossil_plot_data.values)
sizes = sizes[:5] + [sum(sizes[5:])]
labels = list(fossil_plot_data.index)
labels = labels[:5] + ['Other']
colors = [COLOUR_DICT.get(label) for label in labels]
labels = [f'{label}: {round(sizes[i],1)}' if len(label) < 20 else 
f'{label}:\n{round(sizes[i],1)}' for i, label in enumerate(labels)]

fig, ax = plt.subplots(1,2, figsize = (15,6))
squarify.plot(sizes=sizes, ax=ax[0], alpha=0.85, color=colors, label=labels)
ax[0].set_title('Fossil Fuel Consumption - 2019\n(Oil Equivalent/Megatonnes)')
u.format_axes(ax[0])
#plt.show()

## Renewable Consumption
sizes = list(renewable_plot_data.values)
sizes = sizes[:5] + [sum(sizes[5:])]
labels = list(renewable_plot_data.index)
labels = labels[:5] + ['Other']
colors = [COLOUR_DICT.get(label) for label in labels]
labels = [f'{label}: {round(sizes[i],1)}' if len(label) < 20 else f'{label}:\n{round(sizes[i],1)}' for i, label in enumerate(labels)]

#fig, ax = plt.subplots()
squarify.plot(sizes=sizes, ax=ax[1], alpha=0.85, color=colors, label=labels)
ax[1].set_title('Renewable Energy Consumption - 2019\n(Oil Equivalent/Megatonnes)')
u.format_axes(ax[1])
plt.show()
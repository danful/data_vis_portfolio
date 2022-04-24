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

## Load data
emissions_list, emissions_detail_list = emissions.run_process()
fossil_df = fossil.run_process()  # Unit: Mtoe (Megatonnes of oil equivalent)
renewable_df = renewable.run_process()  # Unit: Mtoe

## Transform data
fossil_df = fossil_df.rename(columns = RENAME_DICT)
fossil_df = fossil_df.drop(columns = DROP_COLS)
renewable_df = renewable_df.rename(columns = RENAME_DICT)
renewable_df = renewable_df.drop(columns = DROP_COLS)

total_consumption = fossil_df + renewable_df
renewable_prop_df = renewable_df.div(total_consumption)

## Plotting visualisations
# Bar chart
bar_df = renewable_prop_df.T

fig, ax = plt.subplots(figsize = (6,6))
fig.suptitle('Proportion of Energy Consumption\nfrom Renewable Sources by industry (2019)')
box = ax.get_position()
ax.set_position([box.x0 + 0.2, box.y0, box.width * 0.8, box.height])
sns.barplot(x=bar_df['2019'], y=bar_df.index, data=bar_df, ax=ax, orient='h', color='#33a02c')
ax.set_xlabel('Proportion')
plt.show()

# Box plots
box_df = renewable_prop_df.reset_index()
box_df = pd.melt(box_df, id_vars = 'index', value_vars=fossil_df.columns, var_name='industry', value_name='prop_renewable')

fig, ax = plt.subplots(figsize = (8,6))
ax.set_title('Proportion of Energy Consumption\nfrom Renewable Sources - Annual Development Summary')
sns.boxplot(data = box_df, x='index',y='prop_renewable', ax=ax, color='#33a02c')
ax.set_xticklabels(renewable_prop_df.index, rotation = 45)
ax.set_xlabel('Year')
ax.set_ylabel('Proportion from Renewable Source')
plt.show()

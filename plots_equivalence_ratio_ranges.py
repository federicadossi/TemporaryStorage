# %% This script creates plots that are useful to analyze the equivalence ratio

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Define the directory path
directory_path = r'C:\thesis\python'

# Load the CSV file into a DataFrame
csv_file_path = f'{directory_path}\lashof_joos.csv'
lashof_joos = pd.read_csv(csv_file_path)

# parameters
lower_bound = 99
upper_bound = 101

# Filter the dataframe based on the equivalence ratio
filtered_data = lashof_joos[(lashof_joos['Equivalence Ratio'] >= lower_bound) & (lashof_joos['Equivalence Ratio'] <= upper_bound)]

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['Time Horizon (years)'], filtered_data['Delay (years)'], c=filtered_data['Equivalence Ratio'], cmap='viridis', edgecolor='k')
plt.colorbar(label='Equivalence Ratio')
plt.xlabel('Time Horizon (years)')
plt.ylabel('Delay (years)')
plt.title(f'Time Horizon and Delay for Equivalence Ratio between {lower_bound} and {upper_bound}')
plt.grid(True)
plt.savefig(f'{directory_path}\\EquivalenceRatio.png')
plt.show()

# %%
# # Create the hexbin plot
# plt.figure(figsize=(10, 6))
# hb = plt.hexbin(lashof_joos['Time Horizon (years)'], lashof_joos['Equivalence Ratio'], C=lashof_joos['Delay (years)'], gridsize=50, cmap='viridis', reduce_C_function=np.mean)
# plt.colorbar(hb, label='Delay (years)')
# plt.xlabel('Time Horizon (years)')
# plt.ylabel('Equivalence Ratio')
# plt.title('Hexbin Plot of Time Horizon and Equivalence Ratio with Delays')
# plt.grid(True)
# plt.savefig(f'{directory_path}\\EquivalenceRatioHexbinPlot.png')
# plt.show()


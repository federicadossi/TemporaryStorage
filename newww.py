# %% This script creates plots that are useful to analyze the equivalence ratio

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Define the directory path
directory_path = r'C:\thesis\python'

# Load the CSV file into a DataFrame
csv_file_path = f'{directory_path}\lashof_joos.csv'
lashof_joos = pd.read_csv(csv_file_path)

# Filter the dataframe based on the equivalence ratio
filtered_data = lashof_joos[(lashof_joos['Equivalence Ratio'] >= 8) & (lashof_joos['Equivalence Ratio'] <= 9.5)]

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['Time Horizon (years)'], filtered_data['Delay (years)'], c=filtered_data['Equivalence Ratio'], cmap='viridis', edgecolor='k')
plt.colorbar(label='Equivalence Ratio')
plt.xlabel('Time Horizon (years)')
plt.ylabel('Delay (years)')
plt.title('Time Horizon and Delay for Equivalence Ratio between 8.5 and 9.1')
plt.grid(True)
plt.savefig(f'{directory_path}\\EquivalenceRatio.png')
plt.show()

# %% Filter the dataframe based on the equivalence ratio
filtered_data = lashof_joos[(lashof_joos['Equivalence Ratio'] >= 36) & (lashof_joos['Equivalence Ratio'] <= 38)]

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(filtered_data['Time Horizon (years)'], filtered_data['Delay (years)'], c=filtered_data['Equivalence Ratio'], cmap='viridis', edgecolor='k')
plt.colorbar(label='Equivalence Ratio')
plt.xlabel('Time Horizon (years)')
plt.ylabel('Delay (years)')
plt.title('Time Horizon and Delay for Equivalence Ratio between 36 and 38')
plt.savefig(f'{directory_path}\\EquivalenceRatio37.png')
plt.grid(True)
plt.show()

# %%
# Create the hexbin plot
plt.figure(figsize=(10, 6))
hb = plt.hexbin(lashof_joos['Time Horizon (years)'], lashof_joos['Equivalence Ratio'], C=lashof_joos['Delay (years)'], gridsize=50, cmap='viridis', reduce_C_function=np.mean)
plt.colorbar(hb, label='Delay (years)')
plt.xlabel('Time Horizon (years)')
plt.ylabel('Equivalence Ratio')
plt.title('Hexbin Plot of Time Horizon and Equivalence Ratio with Delays')
plt.grid(True)
plt.savefig(f'{directory_path}\\EquivalenceRatioHexbinPlot.png')
plt.show()


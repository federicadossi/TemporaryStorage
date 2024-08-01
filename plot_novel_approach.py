# %% This script creates plots that are useful to analyze the results of the novel approach

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define the directory path
directory_path = r'C:\thesis\python'

# Load the CSV file into a DataFrame
csv_file_path = f'{directory_path}\\new_approach.csv'
new_approach = pd.read_csv(csv_file_path)
new_approach = new_approach.drop(columns=['Avoided Emission', 'Costs of Release', 'Benefits'])

# %% Define the delay times to plot
delay_times = [10, 50, 100, 200]

# Filter the DataFrame for the specified delay times
filtered_df = new_approach[new_approach['Delay'].isin(delay_times)]

# Create a single plot
plt.figure()

# Plot each delay time on the same axes
for delay in delay_times:
    subset = filtered_df[filtered_df['Delay'] == delay]
    plt.plot(subset['Discount Rate'], subset['Equivalence ratio'], marker='o', linestyle='-', label=f'Delay {delay}')

# Add titles and labels
plt.title('Equivalence Ratio vs Discount Rate for Different Delay Times')
plt.xlabel('Discount Rate')
plt.ylabel('Equivalence Ratio')
plt.legend()
plt.grid(True)
plt.savefig(f'{directory_path}\\EquivalenceRatioNewApproach.png')
plt.show()
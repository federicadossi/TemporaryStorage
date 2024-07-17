# %% This script performs the analysis to correlate a certain discount rate with the time horizon adopted by Lashof method

# Import packages
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import matplotlib


# Define the directory path
directory_path = r'C:\thesis\python'

# Read the CSV files into DataFrames and prepare for analysis
new_approach = pd.read_csv(os.path.join(directory_path, 'new_approach.csv'))
lashof_joos = pd.read_csv(os.path.join(directory_path, 'lashof_JOOS.csv'))
new_approach = new_approach.drop(columns=['Avoided Emission', 'Costs of Release', 'Benefits'])
lashof_joos = lashof_joos.drop(columns=['Costs (ton-years)', 'Benefits (ton-years)'])
lashof_joos = lashof_joos.dropna(subset=['Equivalence Ratio'])

# Initialize a list to store the results
results = []

# Loop through each unique time horizon in lashof_joos
for time_horizon in lashof_joos['Time Horizon (years)'].unique():
    # Filter the lashof_joos dataset by the current time horizon
    filtered_lashof_joos = lashof_joos[lashof_joos['Time Horizon (years)'] == time_horizon]

    # Loop through each delay value
    for delay in filtered_lashof_joos['Delay (years)'].unique():
        # Get the equivalence ratio from lashof_joos for the current time horizon and delay
        lashof_joos_ratio = filtered_lashof_joos[filtered_lashof_joos['Delay (years)'] == delay]['Equivalence Ratio'].values[0]

        # Filter the new_approach dataset by the current delay
        filtered_new_approach = new_approach[new_approach['Delay'] == delay]

        # Initialize variables to store the best discount rate and the smallest difference
        best_discount_rate = None
        smallest_difference = float('inf')

        # Loop through each discount rate in the filtered_new_approach
        for discount_rate in filtered_new_approach['Discount Rate'].unique():
            # Get the equivalence ratio from new_approach for the current discount rate and delay
            new_approach_ratio = filtered_new_approach[filtered_new_approach['Discount Rate'] == discount_rate]['Equivalence ratio'].values[0]

            # Calculate the absolute difference
            difference = abs(new_approach_ratio - lashof_joos_ratio)

            # Check if this is the smallest difference so far
            if difference < smallest_difference:
                smallest_difference = difference
                best_discount_rate = discount_rate

        # Append the results for this combination of time horizon and delay
        results.append({
            'Time Horizon (years)': time_horizon,
            'Delay (years)': delay,
            'Best Discount Rate': best_discount_rate,
            'Smallest Difference': smallest_difference
        })

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(results)
file_name = 'results_analysis2.csv'
results_df.to_csv(f'{directory_path}\\{file_name}', index=False)

# %% Plot 1: Delay and Discount Rate separate plots for each Time Horizon
plt.clf()
# Specify the time horizons of interest
selected_time_horizons = [100, 200, 300, 400, 600, 800]

# Define the number of columns for the grid layout
num_cols = 3
num_rows = (len(selected_time_horizons) + num_cols - 1) // num_cols

# Create a figure with subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Plot each selected time horizon value in a separate subplot
for i, (ax, time_horizon) in enumerate(zip(axes, selected_time_horizons)):
    subset = results_df[results_df['Time Horizon (years)'] == time_horizon]
    ax.scatter(subset['Delay (years)'], subset['Best Discount Rate'])
    ax.set_title(f'Time Horizon: {time_horizon}')
    ax.set_xlabel('Delay (years)')
    ax.set_ylabel('Discount Rate')
    if i < 2:
        ax.set_ylim(0, 0.05)  # y-axis limits for the first two figures
    else:
        ax.set_ylim(0, 0.01)  # y-axis limits for the remaining four figures
    ax.grid(True)

# Remove any unused subplots
for i in range(len(selected_time_horizons), len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.savefig(f'{directory_path}\\R_delay_time_horizon2.png')
plt.show()


# %% Plot 2: Discount Rate and Time Horizon separate plots for each Delay time
# Specify the delays of interest
selected_delays = [10, 30, 70, 100, 150, 200]

# Define the number of columns for the grid layout
num_cols = 3
num_rows = (len(selected_delays) + num_cols - 1) // num_cols

# Create a figure with subplots
plt.clf()
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Plot each selected delay value in a separate subplot
for ax, delay in zip(axes, selected_delays):
    subset = results_df[results_df['Delay (years)'] == delay]
    ax.scatter(subset['Best Discount Rate'], subset['Time Horizon (years)'])
    ax.set_title(f'Delay: {delay}')
    ax.set_xlabel('Discount Rate')
    ax.set_ylabel('Time Horizon (years)')
    ax.set_ylim(0, 1000)  # Set y-axis limits from 0 to 1000
    ax.grid(True)

# Remove any unused subplots
for i in range(len(selected_delays), len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.savefig(f'{directory_path}\\TH_r_delay2.png')
plt.show()

# %% SINGLE PLOTS FOR VALUES OF INTEREST
# Function to plot for a given time horizon
def plot_time_horizon(time_horizon, ylim=None):
    subset = results_df[results_df['Time Horizon (years)'] == time_horizon]
    plt.figure(figsize=(10, 6))
    plt.scatter(subset['Delay (years)'], subset['Best Discount Rate'])
    plt.title(f'Time Horizon: {time_horizon}')
    plt.xlabel('Delay (years)')
    plt.ylabel('Discount Rate')
    if ylim:
        plt.ylim(ylim)
    plt.grid(True)
    plt.savefig(f'{directory_path}\\R_delay_time_horizon_{time_horizon}.png')
    plt.show()
    plt.clf()

# Plot for Time Horizon = 100
plot_time_horizon(100, ylim=(0, 0.05))
# Plot for Time Horizon = 1000
plot_time_horizon(1000, ylim=(0, 0.01))

#%% Plot for DELAY = 100
delay_of_interest = 100

# Subset the DataFrame for the specific delay
subset = results_df[results_df['Delay (years)'] == delay_of_interest]

# Create a new figure
plt.clf()
plt.figure(figsize=(10, 6))

# Create a scatter plot with the time horizon on the x-axis and the discount rate on the y-axis
plt.scatter(subset['Time Horizon (years)'], subset['Best Discount Rate'])

# Set the title and labels
plt.title(f'Delay: {delay_of_interest}')
plt.xlabel('Time Horizon (years)')
plt.ylabel('Discount Rate')
plt.xlim(0, 1010)
# Set the number of grids on the x-axis
ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
plt.grid(True)

# Save the figure
plt.savefig(f'{directory_path}\\TH_r_delay_{delay_of_interest}.png')

# Show the plot
plt.show()




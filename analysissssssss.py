# %% This script performs the analysis to correlate a certain discount rate with the time horizon adopted by Lashof method

# Import packages
import os
import pandas as pd
import matplotlib.pyplot as plt
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

# Initialize a list to store results
results = []

# Loop through each unique discount rate in new_approach
for discount_rate in new_approach['Discount Rate'].unique():
    # Filter the new_approach dataset by the current discount rate
    filtered_new_approach = new_approach[new_approach['Discount Rate'] == discount_rate]

    # Initialize a variable to sum the differences
    total_difference = 0

    # Loop through each delay value
    for delay in filtered_new_approach['Delay'].unique():
        # Ensure the delay exists in both dataframes
        if delay not in lashof_joos['Delay (years)'].values:
            continue  # if delay > time horizon delay is not in df lashof_joos

        # Get the equivalence ratio from new_approach for the current discount rate and delay
        new_approach_ratio = filtered_new_approach[filtered_new_approach['Delay'] == delay]['Equivalence ratio'].values[
            0]

        # Filter the lashof_joos dataset by the current delay
        filtered_lashof_joos = lashof_joos[lashof_joos['Delay (years)'] == delay]

        # Initialize variables to store the best time horizon and the smallest difference
        best_time_horizon = None
        smallest_difference = float('inf')

        # Loop through each time horizon in the filtered_lashof_joos
        for time_horizon in filtered_lashof_joos['Time Horizon (years)'].unique():
            # Get the equivalence ratio from lashof_joos for the current time horizon and delay
            lashof_joos_ratio = \
            filtered_lashof_joos[filtered_lashof_joos['Time Horizon (years)'] == time_horizon]['Equivalence Ratio'].values[0]

            # Calculate the absolute difference
            difference = abs(new_approach_ratio - lashof_joos_ratio)

            # Check if this is the smallest difference so far
            if difference < smallest_difference:
                smallest_difference = difference
                best_time_horizon = time_horizon

        # Append the results to the list
        results.append((discount_rate, delay, best_time_horizon, smallest_difference))

    # Convert results to a dataframe
    results_df = pd.DataFrame(results, columns=['Discount Rate', 'Delay', 'Best Time Horizon', 'Smallest Difference'])

results_df.to_csv(os.path.join(directory_path, 'results_analysis.csv'), index=False)

# %% Understand the relationship between TH, discount rate and delays

# Plot 1: Total Differences for Each Discount Rate
total_differences = results_df.groupby('Discount Rate')['Smallest Difference'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=total_differences, x='Discount Rate', y='Smallest Difference')
plt.title('Total Differences for Each Discount Rate')
plt.xlabel('Discount Rate')
plt.ylabel('Total Difference')
plt.grid(True)
plt.savefig(f'{directory_path}\\total_diff.png')
plt.show()

# %% Plot 2: Discount Rate and Best Time Horizon
plt.figure(figsize=(12, 8))
sns.scatterplot(data=results_df, x='Discount Rate', y='Best Time Horizon', hue='Delay', palette='viridis', legend='full')
plt.title('Scatter Plot of Discount Rate vs. Best Time Horizon')
plt.xlabel('Discount Rate')
plt.ylabel('Best Time Horizon')
plt.legend(title='Delay')
plt.grid(True)
plt.savefig(f'{directory_path}\\TH_r_delay.png')
plt.show()

# # Plot 3: Discount Rate and Best Time Horizon with jittered data
# results_df['Best Time Horizon'] += np.random.normal(0, 5, size=results_df.shape[0])
# results_df['Discount Rate'] += np.random.normal(0, 0.0005, size=results_df.shape[0])
# plt.figure(figsize=(12, 8))
# sns.scatterplot(data=results_df, x='Discount Rate', y='Best Time Horizon', hue='Delay', palette='viridis', legend='full')
# plt.title('Scatter Plot of Discount Rate vs. Best Time Horizon')
# plt.xlabel('Discount Rate')
# plt.ylabel('Best Time Horizon')
# plt.legend(title='Delay')
# plt.grid(True)
# plt.savefig(f'{directory_path}\\TH_r_delay_jittered.png')
# plt.show()

# %% Plot 4: Discount Rate and Best Time Horizon separate plots for each delay time

# Specify the delays of interest
selected_delays = [10, 30, 70, 100, 150, 200]

# Define the number of columns for the grid layout
num_cols = 3
num_rows = (len(selected_delays) + num_cols - 1) // num_cols

# Create a figure with subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# # Determine common y-axis limits
# y_min = results_df['Best Time Horizon'].min()
# y_max = results_df['Best Time Horizon'].max()

# Plot each selected delay value in a separate subplot
for ax, delay in zip(axes, selected_delays):
    subset = results_df[results_df['Delay'] == delay]
    ax.scatter(subset['Discount Rate'], subset['Best Time Horizon'])
    ax.set_title(f'Delay: {delay}')
    ax.set_xlabel('Discount Rate')
    ax.set_ylabel('Best Time Horizon')
    ax.set_ylim(0, 1000)  # Set y-axis limits from 0 to 1000
    ax.grid(True)
    # ax.set_ylim(y_min, y_max)  # Set common y-axis limits

# Remove any unused subplots
for i in range(len(selected_delays), len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.savefig(f'{directory_path}\\TH_r_delay_selected_grid.png')
plt.show()

# %% Plot 5: Delay vs. Best Time Horizon separate plots for each discount rate

# Specify the discount rates of interest
selected_discount_rates = [0.001, 0.003, 0.005, 0.01, 0.02, 0.03]

# Define the number of columns for the grid layout
num_cols = 3
num_rows = (len(selected_discount_rates) + num_cols - 1) // num_cols

# Create a figure with subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5 * num_rows))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Plot each selected discount rate in a separate subplot
for ax, discount_rate in zip(axes, selected_discount_rates):
    subset = results_df[results_df['Discount Rate'] == discount_rate]
    ax.scatter(subset['Delay'], subset['Best Time Horizon'])
    ax.set_title(f'Discount Rate: {discount_rate}')
    ax.set_xlabel('Delay')
    ax.set_ylabel('Best Time Horizon')
    ax.set_ylim(0, 1000)
    ax.grid(True)

# Remove any unused subplots
for i in range(len(selected_discount_rates), len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout()
plt.savefig(f'{directory_path}\\TH_delay_discount_rate_grid.png')
plt.show()

# %% Plot 6: Delay vs. Discount Rate separate plots for each time horizon

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
    subset = results_df[results_df['Best Time Horizon'] == time_horizon]
    ax.scatter(subset['Delay'], subset['Discount Rate'])
    ax.set_title(f'Time Horizon: {time_horizon}')
    ax.set_xlabel('Delay')
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
plt.savefig(f'{directory_path}\\DR_delay_time_horizon_grid.png')
plt.show()

#

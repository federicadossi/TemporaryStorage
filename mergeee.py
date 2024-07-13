import pandas as pd
import os

# Define the directory path
directory_path = r'C:\thesis\python'

# Load the CSV files
lashof_ipcc_path = os.path.join(directory_path, 'lashof_IPCC1990.csv')
moura_costa_ipcc_path = os.path.join(directory_path, 'moura_costa_IPCC1990.csv')
lashof_joos_path = os.path.join(directory_path, 'lashof_JOOS.csv')
moura_costa_joos_path = os.path.join(directory_path, 'moura_costa_JOOS.csv')

lashof_ipcc = pd.read_csv(lashof_ipcc_path)
moura_costa_ipcc = pd.read_csv(moura_costa_ipcc_path)
lashof_joos = pd.read_csv(lashof_joos_path)
moura_costa_joos = pd.read_csv(moura_costa_joos_path)

# Check the content of each dataframe to ensure they are loaded correctly
print("Lashof IPCC DataFrame:")
print(lashof_ipcc.head())

print("\nMoura Costa IPCC DataFrame:")
print(moura_costa_ipcc.head())

print("\nLashof JOOS DataFrame:")
print(lashof_joos.head())

print("\nMoura Costa JOOS DataFrame:")
print(moura_costa_joos.head())

# Rename columns to distinguish methods
lashof_ipcc.columns = ['Time Horizon (years)', 'Delay (years)', 'Costs_Lashof_IPCC (ton-years)', 'Benefits_Lashof_IPCC (ton-years)', 'Equivalence Ratio_Lashof_IPCC']
moura_costa_ipcc.columns = ['Time Horizon (years)', 'Delay (years)', 'Costs_MC_IPCC (ton-years)', 'Benefits_MC_IPCC (ton-years)', 'Equivalence Ratio_MC_IPCC']
lashof_joos.columns = ['Time Horizon (years)', 'Delay (years)', 'Costs_Lashof_JOOS (ton-years)', 'Benefits_Lashof_JOOS (ton-years)', 'Equivalence Ratio_Lashof_JOOS']
moura_costa_joos.columns = ['Time Horizon (years)', 'Delay (years)', 'Costs_MC_JOOS (ton-years)', 'Benefits_MC_JOOS (ton-years)', 'Equivalence Ratio_MC_JOOS']

# Check for matching keys before merging
common_keys = ['Time Horizon (years)', 'Delay (years)']
print("\nCommon keys in Lashof IPCC and Moura Costa IPCC:")
print(set(lashof_ipcc.columns).intersection(set(moura_costa_ipcc.columns)))

print("\nCommon keys in Lashof IPCC and Lashof JOOS:")
print(set(lashof_ipcc.columns).intersection(set(lashof_joos.columns)))

print("\nCommon keys in Moura Costa IPCC and Moura Costa JOOS:")
print(set(moura_costa_ipcc.columns).intersection(set(moura_costa_joos.columns)))

# Merge dataframes on 'Time Horizon (years)' and 'Delay (years)'
merged_df = pd.merge(lashof_ipcc, moura_costa_ipcc, on=common_keys, how='outer')
merged_df = pd.merge(merged_df, lashof_joos, on=common_keys, how='outer')
merged_df = pd.merge(merged_df, moura_costa_joos, on=common_keys, how='outer')

# Save the merged dataframe to a CSV file
merged_output_path = os.path.join(directory_path, 'merged_results_summary.csv')
merged_df.to_csv(merged_output_path, index=False)

# Define the columns for the summary
summary_columns = [
    'Time Horizon (years)', 'Delay (years)',
    'Equivalence Ratio_Lashof_IPCC', 'Equivalence Ratio_MC_IPCC',
    'Equivalence Ratio_Lashof_JOOS', 'Equivalence Ratio_MC_JOOS'
]

# Create summary DataFrame with the specified columns
summary_df = merged_df[summary_columns]

# Filter the DataFrame to create a shorter version
# Select a subset of unique 'Time Horizon (years)'
time_horizons = [100, 300, 500, 900, 1500]

# Select a subset of unique 'Delay (years)'
delays = [10, 50, 100, 200]

# Create a shorter summary DataFrame
summary_short_df = summary_df[
    (summary_df['Time Horizon (years)'].isin(time_horizons)) &
    (summary_df['Delay (years)'].isin(delays))
]

# Print the shorter summary DataFrame
print("\nShorter Summary DataFrame:")
print(summary_short_df)

# Save the shorter summary DataFrame to a CSV file
summary_short_output_path = r'C:\thesis\python\summary_short_results.csv'
summary_short_df.to_csv(summary_short_output_path, index=False)

# Define the columns for the detailed summary
detailed_summary_columns = [
    'Time Horizon (years)', 'Delay (years)',
    'Costs_Lashof_IPCC (ton-years)', 'Benefits_Lashof_IPCC (ton-years)', 'Equivalence Ratio_Lashof_IPCC',
    'Costs_MC_IPCC (ton-years)', 'Benefits_MC_IPCC (ton-years)', 'Equivalence Ratio_MC_IPCC',
    'Costs_Lashof_JOOS (ton-years)', 'Benefits_Lashof_JOOS (ton-years)', 'Equivalence Ratio_Lashof_JOOS',
    'Costs_MC_JOOS (ton-years)', 'Benefits_MC_JOOS (ton-years)', 'Equivalence Ratio_MC_JOOS'
]

# Create detailed summary DataFrame with the specified columns
detailed_summary_df = merged_df[detailed_summary_columns]

# Create a shorter detailed summary DataFrame
detailed_summary_short_df = detailed_summary_df[
    (detailed_summary_df['Time Horizon (years)'].isin(time_horizons)) &
    (detailed_summary_df['Delay (years)'].isin(delays))
]

# Print the shorter detailed summary DataFrame
print("\nShorter Detailed Summary DataFrame:")
print(detailed_summary_short_df)

# Save the shorter detailed summary DataFrame to a CSV file
detailed_summary_short_output_path = r'C:\thesis\python\detailed_summary_short_results.csv'
detailed_summary_short_df.to_csv(detailed_summary_short_output_path, index=False)

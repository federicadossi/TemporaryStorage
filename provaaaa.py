"""
This script analyzes the Impulse Response Function (IRF) as defined by Joos et al. (2013) and IPCC (1990).
It calculates the avoided damages (benefits), costs of release, and equivalence ratios using the Moura-Costa
and Lashof approaches applied to both IRF versions for different time horizons and delay times. Additionally,
it defines and adopts a new approach that uses discount rates instead of time horizons to ensure the integrals
of Joos 2013 are finite. The script calculates benefits, costs, and equivalence ratios for various delays and
discount rates. It saves the results to CSV files for further analysis.
"""

# Import packages
import numpy as np
import os
from scipy.integrate import quad
from functools import partial
import pandas as pd

# Define the directory path
directory_path = r'C:\thesis\python'

# %% NEW APPROACH ON IRF JOOS 2013
# Define the equation DD(t): IRF as formulated in Joos et al. (2013)
def DD(t, t_disc, r):
    term1 = 21.73 * np.exp(-r * t_disc)
    term2 = 22.4 * np.exp(-t / 394.4) * np.exp(-r * t_disc)
    term3 = 28.24 * np.exp(-t / 36.54) * np.exp(-r * t_disc)
    term4 = 27.63 * np.exp(-t / 4.304) * np.exp(-r * t_disc)
    return term1 + term2 + term3 + term4

# Function to integrate for line 1 (benefit from delayed emission)
def integrand_line1(t, r):
    return DD(t, t, r)

# Function to integrate for line 2 (costs of release)
def integrand_line2(t, delay, r):
    t_disc = t + delay
    return DD(t, t_disc, r)

# Prepare to collect results
results = []

# Loop through discount rates and delays
for r in np.arange(0.001, 0.031, 0.0005):
    for delay in range(10, 201, 10):
        # Fix the discount rate and delay for the integrand functions using partial
        integrand_line1_fixed = partial(integrand_line1, r=r)
        integrand_line2_fixed = partial(integrand_line2, delay=delay, r=r)

        # Calculate the area under line 1 from 0 to infinity
        avoided_emission, error1 = quad(integrand_line1_fixed, 0, np.inf)

        # Calculate the area under line 2 from 0 to infinity
        costs_of_release, error2 = quad(integrand_line2_fixed, 0, np.inf)

        # Calculate the equivalence
        benefits = avoided_emission - costs_of_release
        equivalence = avoided_emission / benefits

        # Append results to the list
        results.append({'Discount Rate': r, 'Delay': delay, 'Avoided Emission': avoided_emission,
                        'Costs of Release': costs_of_release, 'Benefits': benefits, 'Equivalence ratio': equivalence})

# Convert results to a DataFrame
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(directory_path, 'new_approach.csv'), index=False)

# %%
'''
OLD APPROACHES ON IRF JOOS 2013
Both MC and Lashof require areas to be finite therefore we adopt time horizons
'''

# Define the UD (Undiscounted Damage) function
def UD(t):
    return 21.73 + 22.4 * np.exp(-t / 394.4) + 28.24 * np.exp(-t / 36.54) + 27.63 * np.exp(-t / 4.304)

# Initialize lists to store the results
moura_costa_results = []
lashof_results = []

#%% Vary delay and time horizon for Moura-Costa method

for time_horizon in range(50, 10000, 50):
    for delay in range(10, 210, 10):
        if time_horizon < delay:
            area_under_UD = float('nan')
            benefits_MC = float('nan')
            equivalence_ratio = float('nan')
        else:
            benefits_MC = delay * 100  # ton-years
            area_under_UD, error = quad(UD, 0, time_horizon)
            equivalence_ratio = area_under_UD / benefits_MC
        moura_costa_results.append([time_horizon, delay, area_under_UD, benefits_MC, equivalence_ratio])

#%% Vary delay and time horizon for Lashof method

for time_horizon in range(50, 10000, 50):
    for delay in range(10, 210, 10):
        if time_horizon < delay:
            equivalence_ratio = float('nan')
            costs_Lashof = float('nan')
            benefits_Lashof = float('nan')
        else:
            area_under_UD, error = quad(UD, 0, time_horizon)
            area_under_UD_DELAYED, error = quad(UD, 0, time_horizon - delay)
            costs_Lashof = area_under_UD
            benefits_Lashof = area_under_UD - area_under_UD_DELAYED
            equivalence_ratio = costs_Lashof / benefits_Lashof
        lashof_results.append([time_horizon, delay, costs_Lashof, benefits_Lashof, equivalence_ratio])

# Convert results to dataframes
moura_costa_joos = pd.DataFrame(moura_costa_results,
                              columns=['Time Horizon (years)', 'Delay (years)', 'Costs (ton-years)', 'Benefits (ton-years)',
                                       'Equivalence Ratio'])
lashof_joos = pd.DataFrame(lashof_results,
                         columns=['Time Horizon (years)', 'Delay (years)', 'Costs (ton-years)', 'Benefits (ton-years)',
                                  'Equivalence Ratio'])

# Save the dataframes to CSV files
file_name = 'moura_costa_JOOS.csv'
moura_costa_joos.to_csv(f'{directory_path}\\{file_name}', index=False)
file_name = 'lashof_JOOS.csv'
lashof_joos.to_csv(f'{directory_path}\\{file_name}', index=False)

# %% Compute the results for time horizon 100,000 for Lashof method
time_horizon = 100000
lashof_results_100k = []

for delay in range(10, 210, 10):
    if time_horizon < delay:
        equivalence_ratio = float('nan')
        costs_Lashof = float('nan')
        benefits_Lashof = float('nan')
    else:
        area_under_UD, error = quad(UD, 0, time_horizon)
        area_under_UD_DELAYED, error = quad(UD, 0, time_horizon - delay)
        costs_Lashof = area_under_UD
        benefits_Lashof = area_under_UD - area_under_UD_DELAYED
        equivalence_ratio = costs_Lashof / benefits_Lashof
    lashof_results_100k.append([time_horizon, delay, costs_Lashof, benefits_Lashof, equivalence_ratio])

# Convert results to dataframe and save
lashof_results_100k = pd.DataFrame(lashof_results_100k,
                              columns=['Time Horizon (years)', 'Delay (years)', 'Costs (ton-years)', 'Benefits (ton-years)',
                                       'Equivalence Ratio'])
file_name = 'lashof_100k.csv'
lashof_results_100k.to_csv(f'{directory_path}\\{file_name}', index=False)


# %%
'''
OLD APPROACHES ON IRF IPCC 1990
Still adopting time horizons, Lashof always requires time horizons, the ER that is obtained by Moura-Costa whn the TH 
is extended to infinite is calculated.
'''

# Define the function A(t): IRF as formulated in IPCC (1990)
def A(t):
    return 0.30036 * np.exp(-t / 6.6993) + 0.34278 * np.exp(-t / 71.109) + 0.35686 * np.exp(-t / 815.727)

# Vary delay for Moura-Costa to infinite
area_under_A_inf, error = quad(A, 0, np.inf)  # Integrate A(t) over the range from 0 to infinity
print(f"The area under IRF (IPCC1990) from 0 to infinity is {area_under_A_inf:.2f} ton-years.")
moura_costa_results_to_infinite = []
for delay in range(10, 210, 10):
    benefits_MC = delay  # ton-years
    equivalence_ratio = area_under_A_inf / benefits_MC
    moura_costa_results_to_infinite.append([delay, area_under_A_inf, benefits_MC, equivalence_ratio])

# Convert the list to a DataFrame
moura_costa_results_to_infinite = pd.DataFrame(moura_costa_results_to_infinite, columns=['delay', 'area_under_A_inf', 'benefits_MC', 'equivalence_ratio'])
# Save the dataframes to CSV files
moura_costa_results_to_infinite.to_csv(os.path.join(directory_path, 'moura_costa_infinite.csv'), index=False)

# Initialize lists to store the results
moura_costa_results = []
lashof_results = []

# Vary delay for Moura-Costa method from 10 to 100 years (every 10 years)
for time_horizon in range(100, 10000, 200):
    for delay in range(10, 210, 10):
        if time_horizon < delay:
            area_under_A = float('nan')
            benefits_MC = float('nan')
            equivalence_ratio = float('nan')
        else:
            area_under_A, error = quad(A, 0, time_horizon)
            benefits_MC = delay  # ton-years
            equivalence_ratio = area_under_A / benefits_MC
        moura_costa_results.append([time_horizon, delay, area_under_A, benefits_MC, equivalence_ratio])

# Vary time horizon for Lashof method from 100 to 3000 years (every 200 years) and delays from 10 to 100 (every 10 years)
for time_horizon in range(100, 10000, 200):
    for delay in range(10, 210, 10):
        if time_horizon < delay:
            equivalence_ratio = float('nan')
            costs_Lashof = float('nan')
            benefits_Lashof = float('nan')
        else:
            area_under_A, error = quad(A, 0, time_horizon)
            area_under_A_DELAYED, error = quad(A, 0, time_horizon - delay)
            costs_Lashof = area_under_A
            benefits_Lashof = area_under_A - area_under_A_DELAYED
            equivalence_ratio = costs_Lashof / benefits_Lashof
        lashof_results.append([time_horizon, delay, costs_Lashof, benefits_Lashof, equivalence_ratio])

# Convert results to dataframes
moura_costa_IPCC = pd.DataFrame(moura_costa_results,
                              columns=['Time Horizon (years)','Delay (years)', 'Costs (ton-years)', 'Benefits (ton-years)',
                                       'Equivalence Ratio'])
lashof_IPCC = pd.DataFrame(lashof_results,
                         columns=['Time Horizon (years)', 'Delay (years)', 'Costs (ton-years)', 'Benefits (ton-years)',
                                  'Equivalence Ratio'])

# Save the dataframes to CSV files
moura_costa_IPCC.to_csv(os.path.join(directory_path, 'moura_costa_IPCC1990.csv'), index=False)
lashof_IPCC.to_csv(os.path.join(directory_path, 'lashof_IPCC1990.csv'), index=False)
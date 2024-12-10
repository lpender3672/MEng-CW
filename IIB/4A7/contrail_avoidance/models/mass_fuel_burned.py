
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
# load pd from txt

adf = pd.read_csv("IIB/4A7/contrail_avoidance/data/aircraft.txt", delimiter="\t")

fdf = pd.read_csv("IIB/4A7/contrail_avoidance/data/Flights_20150601_20150630.csv")

NM_TO_KM = 1.852

stupid_fucking_mapping = {
    'A333': 'A330-300',
    'A332': 'A330-200',
    'B788': 'B787-8',
    'B789': 'B787-9',
    'B77W': 'B777-300ER',
    'B772': 'B777-200',
    'A388': 'A380',
    'B763': 'B767-300',
    'B738': 'B737-800',
    'A321': 'A321',
    'A220-100': 'BCS1',
    'A220-300': 'BCS3',
    'A320' : 'A320',
}

print(adf['ICAO '])

adf.columns = adf.columns.str.strip()
fdf.columns = fdf.columns.str.strip()


fdf['Mapped AC Type'] = fdf['AC Type'].map(stupid_fucking_mapping)


merged_df = fdf.merge(adf, left_on='Mapped AC Type', right_on='ICAO', how='left')

#merged_df.to_csv("fuel_burn_results.csv", index=False)
unmatched = merged_df[merged_df['ICAO'].isnull()]
print(unmatched['AC Type'].unique())

matched = merged_df[merged_df['ICAO'].notnull()]

correction_ratio = fdf['Actual Distance Flown (nm)'].sum() / matched['Actual Distance Flown (nm)'].sum()


flight_fuels_kg = matched['Fuel Burn'] * matched['Actual Distance Flown (nm)'] * NM_TO_KM
total_mass_fuel = correction_ratio * flight_fuels_kg.sum()

print(f"Total mass kerosine burned: {total_mass_fuel * 12 * 1e-12} Gt")

kerosine_emissions_factor = 3.15

print(f"CO2 emissions {kerosine_emissions_factor * total_mass_fuel * 12 * 1e-12} Gt")

sorted_df = fdf.sort_values('Actual Distance Flown (nm)').head()
# create bar chat of top 10 
fig, ax = plt.subplots()
ax.bar(np.arange(0, 5, 1), sorted_df['Actual Distance Flown (nm)'], sorted_df['Mapped AC Type'])

plt.show()

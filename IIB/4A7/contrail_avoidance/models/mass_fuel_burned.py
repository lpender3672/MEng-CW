
import pandas as pd
import numpy as np

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

merged_df.to_csv("fuel_burn_results.csv", index=False)

unmatched = merged_df[merged_df['ICAO'].isnull()]

print(unmatched['AC Type'].unique())
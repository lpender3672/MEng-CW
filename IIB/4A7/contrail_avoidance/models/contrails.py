# pycontrails
import pandas as pd
import numpy as np

from pycontrails import Flight
from pycontrails.datalib.ecmwf import ERA5
from pycontrails.models.cocip import Cocip
from pycontrails.models.humidity_scaling import ConstantHumidityScaling
from pycontrails.physics import units


from pycontrails import DiskCacheStore

import matplotlib.pyplot as plt

# set up the cache
cache = DiskCacheStore("cache")

df_flight = pd.read_csv("IIB/4A7/contrail_avoidance/data/flight-cocip.csv")
df_flight.head()

attrs = {
    "flight_id": "fid",
    "aircraft_type": df_flight["ICAO Aircraft Type"].values[0],
    "wingspan": df_flight["Wingspan (m)"].values[0],
}

df_flight["time"] = pd.to_datetime(df_flight["UTC time"], origin="unix", unit="s")
df_flight["altitude"] = units.ft_to_m(df_flight["Altitude (feet)"])
df_flight = df_flight.rename(
    columns={
        "Longitude (degrees)": "longitude",
        "Latitude (degrees)": "latitude",
        "True airspeed (m s-1)": "true_airspeed",
        "Mach Number": "mach_number",
        "Aircraft mass (kg)": "aircraft_mass",
        "Fuel mass flow rate (kg s-1)": "fuel_flow",
        "Overall propulsion efficiency": "engine_efficiency",
        "nvPM number emissions index (kg-1)": "nvpm_ei_n",
    }
)

df_flight = df_flight.drop(
    columns=["ICAO Aircraft Type", "Wingspan (m)", "UTC time", "Altitude (feet)"]
)

fl = Flight(data=df_flight, attrs=attrs)
print(fl)

time = (
    pd.to_datetime(fl["time"][0]).floor("h"),
    pd.to_datetime(fl["time"][-1]).ceil("h") + pd.Timedelta("10h"),
)

# select pressure levels
pressure_levels = [
    400,
    350,
    300,
    250,
    225,
    200,
    175,
    150,
]

era5pl = ERA5(
    time=time, 
    variables=Cocip.met_variables, 
    pressure_levels=pressure_levels,
    cachestore=cache,
    )
era5sl = ERA5(
    time=time,
    variables=Cocip.rad_variables,
    cachestore=cache,
    )

met = era5pl.open_metdataset()
rad = era5sl.open_metdataset()


params = {
    "process_emissions": False,
    "verbose_outputs": True,
    "humidity_scaling": ConstantHumidityScaling(rhi_adj=0.98),
}
cocip = Cocip(met=met, rad=rad, params=params)

fl_out = cocip.eval(source=fl)

# get dataframe of flight 0
df = fl_out.dataframe

print(df.head())

ax = plt.axes()

cocip.source.dataframe.plot(
    "longitude",
    "latitude",
    color="k",
    ax=ax,
    label="Flight path",
)
cocip.contrail.plot.scatter(
    "longitude",
    "latitude",
    c="rf_lw",
    cmap="Reds",
    ax=ax,
    label="Contrail LW RF",
)
ax.legend();


plt.show()
# pycontrails
import pandas as pd
from matplotlib import pyplot as plt

from pycontrails import Flight
from pycontrails.models.ps_model import PSFlight

from pycontrails.models.cocip import Cocip

from pycontrails.datalib.ecmwf import ERA5
from pycontrails.models.ps_model import PSGrid

from pycontrails import DiskCacheStore

cache = DiskCacheStore("cache")

attrs = {"flight_id": "1", "aircraft_type": "A320"}
flight = Flight(data=pd.read_csv("IIB/4A7/contrail_avoidance/data/flight-ap.csv"), attrs=attrs)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
flight.plot(ax=ax1)
flight.plot_profile(ax=ax2)

plt.tight_layout()

plt.show()

# Create PS Flight model and evaluate
ps_model = PSFlight(
    fill_low_altitude_with_isa_temperature=True,  # Estimate temperature using ISA
    fill_low_altitude_with_zero_wind=True,  # Estimate airspeed by using groundspeed
)
out = ps_model.eval(flight)

# Visualize outputs
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
out.dataframe.plot(x="time", y="aircraft_mass", ax=ax1)
out.dataframe.plot(x="time", y="engine_efficiency", ax=ax2)
out.dataframe.plot(x="time", y="fuel_flow", ax=ax3)
out.dataframe.plot(x="time", y="thrust", ax=ax4)

plt.tight_layout()

plt.show()



# Load meteorology data
time = "2020-03-01 07:00:00"
pressure_levels = [250]
variables = ["air_temperature"]

era5 = ERA5(time=time, variables=Cocip.met_variables, pressure_levels=pressure_levels, cachestore=cache)
met = era5.open_metdataset()

# Run PSGrid model
model = PSGrid(met, aircraft_type="A320")
out = model.eval()

# Visualize outputs
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

out["aircraft_mass"].data.plot(x="longitude", y="latitude", ax=ax1)
ax1.set_title(f"Nominal aircraft mass [kg]\n at pressure level {out.data['level'].values[0]} hPa")

out["fuel_flow"].data.plot(x="longitude", y="latitude", ax=ax2)
ax2.set_title(f"Nominal fuel flow [kg/s]\n at pressure level {out.data['level'].values[0]} hPa")

plt.tight_layout()

plt.show()
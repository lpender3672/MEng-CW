# pycontrails
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pycontrails import Fleet, Flight
from pycontrails.datalib.ecmwf import ERA5, ERA5ModelLevel
from pycontrails.models.cocip import Cocip
from pycontrails.models.humidity_scaling import HistogramMatching
from pycontrails.models.ps_model import PSFlight

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pycontrails.datalib import goes

from pycontrails import DiskCacheStore

cache = DiskCacheStore("cache")

url = "https://confluence.ecmwf.int/display/UDOC/L137+model+level+definitions"
df = pd.read_html(url, na_values="-", index_col="n")[0].rename_axis("model_level")
df.loc[70:90]  # model levels 70 - 90 agree with our ERA5ModelLevel object below


time = ("2024-01-15T00", "2024-01-15T18")

era5ml = ERA5ModelLevel(
    time=time,
    variables=("t", "q", "u", "v", "w", "ciwc"),
    grid=1,  # horizontal resolution, 0.25 by default
    model_levels=range(70, 91),
    pressure_levels=np.arange(170, 400, 10),
    cachestore=cache,
)
met = era5ml.open_metdataset()


era5sl = ERA5(
    time=time,
    variables=("tsr", "ttr"),
    grid=1,
    pressure_levels=-1,
    cachestore=cache,
)
rad = era5sl.open_metdataset()

da = met.data["air_temperature"]
da.isnull().groupby("level").mean(...).plot()
plt.ylabel("Proportion of missing values")
plt.title("Missing values by pressure level");

plt.show()

# There are no missing values above 310 hPa
tmp = da.isnull().isel(time=0).sel(level=slice(310, None))
tmp.plot(x="longitude", y="latitude", add_colorbar=False, col="level", col_wrap=3)
plt.gcf().suptitle("Position of missing values by pressure level", y=1.02);

plt.show()

df = pd.read_csv("https://apidocs.contrails.org/_static/fleet_sample.csv", parse_dates=["time"])
df["time"] = df["time"].dt.tz_convert(None)
df = df.rename(columns={"altitude": "altitude_ft"})

# Artificially shift time to the date of interest
df["time"] = df["time"] + (pd.Timestamp("2024-01-15") - df["time"].min())

# Convert to a pycontrails Fleet instance, keeping only aircraft type covered by the PS model
ps_flight = PSFlight()
flights = []
for flight_id, group in df.groupby("flight_id"):
    aircraft_type = group["aircraft_type"].iloc[0]
    if not ps_flight.check_aircraft_type_availability(aircraft_type, raise_error=False):
        continue

    engine_uid = group["engine_uid"].iloc[0]
    group = group.drop(columns=["aircraft_type", "engine_uid", "flight_id"])
    flight = Flight(group, aircraft_type=aircraft_type, engine_uid=engine_uid, flight_id=flight_id)
    flights.append(flight)

fleet = Fleet.from_seq(flights)

ax = plt.subplot()
for flight in flights:
    flight.plot(ax=ax, alpha=0.3)

plt.show()



handler = goes.GOES(region="C", channels=("C01", "C02", "C03"))
da = handler.get("2024-01-15T20:00:00")

rgb, src_crs, src_extent = goes.extract_goes_visualization(da, color_scheme="true")

dst_crs = ccrs.PlateCarree()

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(projection=dst_crs, extent=(-125, -55, 12, 50))
ax.coastlines(resolution="50m", color="black", linewidth=0.5)

# add state boundaries to plot
ax.add_feature(cfeature.STATES, edgecolor="black", linewidth=0.5)

ax.imshow(rgb, extent=src_extent, transform=src_crs, origin="upper", interpolation="none", alpha = 0.6)



cocip = Cocip(
    met=met,
    rad=rad,
    dt_integration="5 min",
    max_age="12 hours",
    aircraft_performance=PSFlight(),
    humidity_scaling=HistogramMatching(),
)
cocip_pred = cocip.eval(fleet)
contrail = cocip.contrail

# get radiative forcing
print(contrail)
print(contrail["rf_net"].sum())

for flight in flights:
    flight.plot(ax=ax, color="white", linewidth = 0.5, alpha = 0.5)

contrail.plot.scatter(
    x="longitude",
    y="latitude",
    s=contrail["width"] / 100000,
    c=contrail["tau_contrail"],
    vmin=0,
    vmax=0.3,
    alpha=0.1,
    zorder=2,
    ax=ax,
);

# xticks
plt.xticks(np.arange(-125, -55, 5))
plt.xlabel("Longitude")

plt.savefig("IIB/4A7/contrail_avoidance/figures/contrail_map.png", dpi = 400)
plt.show()

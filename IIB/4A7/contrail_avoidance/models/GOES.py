# pycontrails
import numpy as np
import pandas as pd

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pycontrails.datalib import goes

import matplotlib.pyplot as plt


handler = goes.GOES(region="C", channels=("C01", "C02", "C03"))

# Download the data

df_flight = pd.read_csv("IIB/4A7/contrail_avoidance/data/flight-cocip.csv")

time = pd.to_datetime(df_flight["UTC time"], origin="unix", unit="s")[0]

da = handler.get("2024-02-05T20:00:00")
#strtime = time.strftime("%Y-%m-%dT18:00:00")
#print(strtime)
#da = handler.get(strtime)

print(da)


rgb, src_crs, src_extent = goes.extract_goes_visualization(da, color_scheme="true")

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(rgb, origin="upper");

plt.show()

dst_crs = ccrs.PlateCarree()

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(projection=dst_crs, extent=(-125, -55, 12, 50))
ax.coastlines(resolution="50m", color="black", linewidth=0.5)

# add state boundaries to plot
ax.add_feature(cfeature.STATES, edgecolor="black", linewidth=0.5)

ax.imshow(rgb, extent=src_extent, transform=src_crs, origin="upper", interpolation="none")

# Set the x and y ticks to use latitude and longitude labels
gl = ax.gridlines(draw_labels=True, alpha=0.5, linestyle=":")
gl.top_labels = False
gl.right_labels = False

plt.show()

handler = goes.GOES(region="conus", channels=("C11", "C14", "C15"))

# Download the data
da = handler.get("2023-02-09T18:00:00")

rgb, src_crs, src_extent = goes.extract_goes_visualization(da, color_scheme="ash")

fig = plt.figure(figsize=(16, 8))
ax = fig.add_subplot(projection=dst_crs, extent=(-125, -55, 12, 50))
ax.coastlines(resolution="50m", color="black", linewidth=0.5)

# add state boundaries to plot
ax.add_feature(cfeature.STATES, edgecolor="black", linewidth=0.5)

ax.imshow(rgb, extent=src_extent, transform=src_crs, origin="upper", interpolation="none")

# Set the x and y ticks to use latitude and longitude labels
gl = ax.gridlines(draw_labels=True, alpha=0.5, linestyle=":")
gl.top_labels = False
gl.right_labels = False

plt.show()

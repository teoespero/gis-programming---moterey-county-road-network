# Monterey County Road Map
# Author: Teo Espero

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Grab Monterey County roads from the Census Bureau.
url = "https://www2.census.gov/geo/tiger/TIGER2025/ROADS/tl_2025_06053_roads.zip"
roads = gpd.read_file(url)

# Keep highways and local streets.
# These describe road types, not who maintains them.
road_types = {
    "S1100": "Primary highway",
    "S1200": "Secondary highway",
    "S1400": "Local road / city street"
}

# Leave out trails, ramps, alleys, and the other road types.
roads = roads[roads["MTFCC"].isin(road_types)].copy()

# Use readable names in the legend.
roads["road_type"] = roads["MTFCC"].map(road_types)

# Match the coordinate system used by the basemap.
roads_web = roads.to_crs(epsg=3857)

# Draw the roads and give each type a different color.
ax = roads_web.plot(
    column="road_type",          # Color roads by their type.
    categorical=True,           # Treat each type as a separate group.
    legend=True,                # Show the road types in the legend.
    legend_kwds={
        "title": "Road type",
        "fontsize": 9
    },
    cmap="Set1",                 # Use colors that are easy to tell apart.
    figsize=(12, 12),
    linewidth=0.6
)

# Add a light gray basemap behind the roads.
ctx.add_basemap(
    ax,
    source=ctx.providers.Esri.WorldGrayCanvas
)

plt.title("Monterey County Highways and Local Streets")
plt.axis("off")                  # Hide the coordinate axes.

# Put the author and road data source below the map.
plt.gcf().text(
    0.5, 0.02,
    "Map by Teo Espero | Road data: U.S. Census Bureau, 2025 TIGER/Line",
    ha="center",
    fontsize=8
)

plt.show()                      # Show the finished map.
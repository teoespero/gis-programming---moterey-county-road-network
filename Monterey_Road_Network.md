# Monterey County Road Network

**Author: Teo Espero**

## Project screenshot

![Monterey County road map and Python script in PyCharm](monterey_roads_screenshot.png)

Keep the screenshot PNG beside this Markdown file so the image displays.

## What this project does

This script loads Monterey County road data, keeps three road categories, and draws them over a light gray basemap. It uses GeoPandas, Matplotlib, and Contextily. The screenshot shows the script running in PyCharm.

## Set it up

In your PyCharm terminal, run the command below. Save the script as MontereyRoadNetwork.py and run it. You need an internet connection to load the road data and basemap.

```bash
/home/support/PycharmProjects/WelcomeScreen/.venv/bin/python -m pip install geopandas matplotlib contextily
```

## Full script

```python
# Monterey County Road Map
# Author: Teo Espero

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Grab Monterey County roads from the Census Bureau.
url = "https://www2.census.gov/geo/tiger/TIGER2025/ROADS/tl_2025_06053_roads.zip"
roads = gpd.read_file(url)

# These are road types, not the agencies that maintain them.
road_types = {
    "S1100": "Primary highway",
    "S1200": "Secondary highway",
    "S1400": "Local road / city street"
}

# Leave out trails, ramps, alleys, and other road types.
roads = roads[roads["MTFCC"].isin(road_types)].copy()
roads["road_type"] = roads["MTFCC"].map(road_types)

# Match the coordinate system used by the basemap.
roads_web = roads.to_crs(epsg=3857)

# Give each road type a different color.
ax = roads_web.plot(
    column="road_type",          # Pick colors using this column.
    categorical=True,           # Treat the types as separate groups.
    legend=True,                # Explain the colors on the map.
    legend_kwds={"title": "Road type", "fontsize": 9},
    cmap="Set1",                # Choose a color palette.
    figsize=(12, 12),            # Set the figure size in inches.
    linewidth=0.6               # Keep the lines thin.
)

# Put a light gray basemap behind the roads.
ctx.add_basemap(ax, source=ctx.providers.Esri.WorldGrayCanvas)

plt.title("Monterey County Highways and Local Streets")
plt.axis("off")                  # Hide the coordinate axes.

# Add the author and road data source below the map.
plt.gcf().text(
    0.5, 0.02,
    "Map by Teo Espero | Road data: U.S. Census Bureau, 2025 TIGER/Line",
    ha="center", fontsize=8
)

plt.show()                      # Show the finished map.
```

## 1. Import the libraries

GeoPandas reads and works with the road shapes. Matplotlib draws the figure, title, and author credit. Contextily adds the basemap.

## 2. Load the road data

gpd.read_file(url) reads the zipped Census shapefile into a GeoDataFrame named roads. Think of a GeoDataFrame as a table with an extra column holding shapes. Here, those shapes are road lines. The county code 06053 identifies Monterey County, California.

## 3. Choose the road types

The road_types dictionary pairs Census MTFCC codes with readable names. S1100 means primary highway, S1200 means secondary highway, and S1400 means local road or city street. These codes describe road categories; they do not identify state, county, or city ownership.

## 4. Filter the table

isin(road_types) checks whether each MTFCC code is one of the dictionary keys. The brackets keep matching rows. copy() makes a separate table for the roads we want. Trails, ramps, alleys, and other categories are left out.

## 5. Add readable names

map(road_types) looks up each code and writes its matching name into the new road_type column. That gives us a legend people can read without knowing the Census codes.

## 6. Match the basemap

to_crs(epsg=3857) changes the road coordinates to Web Mercator, the coordinate system used by these web tiles. This lets the roads line up with the basemap. For a later road-length calculation, use a suitable local projected CRS, such as EPSG:26910, rather than measuring in Web Mercator.

## 7. Draw the roads

plot() draws the road lines. column chooses the field used for colors. categorical=True treats each road type as its own group. legend=True displays the groups. cmap selects the palette, figsize sets the figure size, and linewidth controls how thick the roads look. ax holds the map area so the basemap can be added to the same figure.

## 8. Add the background and credits

ctx.add_basemap() adds Esri’s light gray tiles behind the roads. plt.title() adds the heading, and plt.axis("off") hides the coordinate axes. plt.gcf().text() places the author and Census source below the map. Contextily also adds the basemap attribution. plt.show() displays the figure.

## What the map tells us

The different colors separate highways from local streets. Dense clusters show places with more mapped road lines. This map does not show traffic counts, pavement condition, or which agency maintains a road. Roads stop at the county boundary because this file only covers Monterey County.

## Issues we ran into

A ModuleNotFoundError for contextily meant it was missing from the project’s virtual environment. Installing it with that environment’s Python fixed the import. OpenStreetMap returned 403 blocked tiles, so we switched providers. The final script uses Esri.WorldGrayCanvas. Tile access still depends on the provider and your connection; switching providers does not guarantee access. If the map looks cut at the county edge, that is the limit of the county road file, not necessarily a plotting error.

## Casual post

Continuing with GeoDataFrames and plotting, I took the road data into PyCharm and mapped Monterey County’s highways and local streets using Python.

I used Census road data, gave each road type a different color, and added a light gray basemap. Had a few hiccups getting the basemap to work, but got there!

Pretty cool seeing familiar places show up in something you built with code.

#Python #GeoPandas #GIS #MontereyCounty #LearningByDoing

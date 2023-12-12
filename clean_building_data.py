""" This script cleans and reduces the NYC Open Data 'building.csv' file.
I want to explore the building location and height data.
Scatch code right now :|
"""

import pandas as pd
import numpy as np
import re

# Needing a function transforms building geometry to mean longitude and latitude
geom = pd.read_csv('./building.csv', usecols=['the_geom'], dtype={'the_geom': 'string'})
g10 = geom[:10]

del geom


def simplify_geom(xi):
    longitude = []
    latitude = []

    coords = re.sub("[()'MULTIPOLYGON]", "", xi).split(',')
    for i in coords:
        lg, lat = i.split()
        longitude.append(float(lg))
        latitude.append(float(lat))
    return np.mean(longitude), np.mean(latitude)


# Works
g10['location'] = g10.the_geom.apply(simplify_geom)

g10['long'], g10['lat'] = zip(*g10.location)

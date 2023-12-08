"""This script cleans and reduces the NYC Open Data 'building.csv' file.
I want to explore the building location and height data. Scatch code right now :/ """

import pandas as pd

# Needing a function transforms building geometry to mean longitude and latitude
geom = pd.read_csv('./building.csv', usecols=['the_geom'], dtype={'the_geom': 'string'})
g10 = geom[:10]

del geom

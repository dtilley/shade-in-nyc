"""This script cleans and reduces the NYC Open Data 'building.csv' file.
   The resulting csv will be loaded into Tableau.
   The data was downloaded from the following link:
   'https://data.cityofnewyork.us/Housing-Development/Building-Footprints/nqwf-w8eh'
"""
import pandas as pd
import numpy as np
import re


# Load useful columns and specify dtypes
cols = ['the_geom',
        'NAME',
        'BIN',
        'CNSTRCT_YR',
        'DOITT_ID',
        'HEIGHTROOF',
        'FEAT_CODE',
        'GROUNDELEV']

dtypes = {'the_geom': 'string',
          'NAME': 'string',
          'BIN': 'string',
          'DOITT_ID': int,
          'HEIGHTROOF': float,
          'FEAT_CODE': 'string',
          'GROUNDELEV': float}

geom = pd.read_csv('./building.csv', usecols=cols, dtype=dtypes)

# CNSTRCT_YR has NaNs for when the construction year is unknown
# CNSTRCT_YR should be 'int64', but I'll address in Tableau
geom.CNSTRCT_YR.isna().sum()  # 10469 structures
geom.CNSTRCT_YR.fillna(value=0, inplace=True)  # fill with 0
geom.CNSTRCT_YR.astype('int64', copy=False)

# Take first 10 rows for debugging
g10 = geom[:10].copy()

# del geom  # for IPython speed while testing

# Select structures taller than minimum 3 story.
geom = geom.loc[geom.HEIGHTROOF >= 30.0].copy()


def simplify_geom(xi):
    """Calculates the centroid of the shape polygon."""
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

geom['location'] = geom.the_geom.apply(simplify_geom)
geom['long'], geom['lat'] = zip(*geom.location)

# Drop original and intermediate columns
g10.drop(['the_geom', 'location'], axis=1, inplace=True)

geom.drop(['the_geom', 'location'], axis=1, inplace=True)

# Borough key
boroughs = {'1': 'Manhattan',
            '2': 'Bronx',
            '3': 'Brooklyn',
            '4': 'Queens',
            '5': 'Staten Island'
            }


# Add borough from BIN
g10['borough'] = g10.BIN.apply(lambda x: boroughs[x[0]])

geom['borough'] = geom.BIN.apply(lambda x: boroughs[x[0]])

# Write csv for Tableau
geom.to_csv('building_location.csv', index=False)

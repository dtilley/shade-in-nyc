""" This script cleans and reduces the NYC Open Data 'building.csv' file.
I want to explore the building location and height data.
Less scatch-like code now :|
"""

import pandas as pd
import numpy as np
import re


# Load useful columns and try specifying dtypes

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

# Needing a function transforms building geometry to mean longitude and latitude
geom = pd.read_csv('./building.csv', usecols=cols, dtype=dtypes)

# CNSTRCT_YR has NaNs for when the construction year is unknown
geom.CNSTRCT_YR.isna().sum() # 10469 structures
geom.CNSTRCT_YR.fillna(value=0, inplace=True) # fill with 0
geom.CNSTRCT_YR.astype('int64', copy=False)

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

# Drop redundent and unused columns
g10.drop(['the_geom', 'location'])

# Add borough

boroughs = {'1': 'Manhattan',
            '2': 'Bronx',
            '3': 'Brooklyn',
            '4': 'Queens',
            '5': 'Staten Island'
            }

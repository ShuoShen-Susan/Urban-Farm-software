#!/usr/bin/env python
# Lint as: python3
"""Map an expression.

Computes the mean NDVI and SAVI by mapping an expression over a collection
and taking the mean.  This intentionally exercises both variants of
Image.expression.
"""

import datetime
import ee
import ee.mapclient
import matplotlib.pyplot as plt

ee.Authenticate()  #"please click the link above to authorize your program"

ee.Initialize()

# Filter the L7 collection to a single month.
collection = (ee.ImageCollection("USDA/NAIP/DOQQ")
              .filterDate(datetime.datetime(2018, 1, 1),
                          datetime.datetime(2018, 12, 31)))


def NDVI(image):
  """A function to compute NDVI."""
  return image.expression('float(b("N") - b("R")) / (b("N") + b("R"))')


def SAVI(image):
  """A function to compute Soil Adjusted Vegetation Index."""
  return ee.Image(0).expression(
      '(1 + L) * float(nir - red)/ (nir + red + L)',
      {
          'nir': image.select('N'),
          'red': image.select('R'),
          'L': 0.2
      })

vis = {
    'min': 0,
    'max': 1,
    'palette': [
        'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163',
        '99B718', '74A901', '66A000', '529400', '3E8601',
        '207401', '056201', '004C00', '023B01', '012E01',
        '011D01', '011301'
    ]}

ee.mapclient.centerMap(-73.9958, 40.7278)
ee.mapclient.addToMap(collection.map(NDVI).mean(), vis)
ee.mapclient.addToMap(collection.map(SAVI).mean(), vis)

print("finish")
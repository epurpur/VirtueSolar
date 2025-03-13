import pandas as pd
import geopandas as gpd
import numpy as np


### import county geopackage datasets
rockingham = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_rockingham.gpkg")

print(f'There are {rockingham.shape[0]} parcels in Rockingham County')


### look at zoning for each county/city
"""
Rockingham zoning values in "zoning" column
['TOWN',
 'A1',
 'A2',
 None,
 'I1',
 'S1',
 'C1',
 'PMF',
 'PCD',
 'I2',
 'PSF']
"""

#removing unwanted zoning from each county
print()
print('Removing parcels with unwanted zoning from each county')
print()

unwanted_zoning = ['TOWN',
 'A1',
 'A2',
 None,
 'I1',
 'S1',
 'C1',
 'PMF',
 'PCD',
 'I2',
 'PSF']

rockingham = rockingham[~rockingham['zoning'].isin(unwanted_zoning)]

print('After zoning filter...')
print(f'There are {rockingham.shape[0]} parcels in Rockingham County')


### Remove properties where mailing address is not local address. This is because we want to focus on primary residences
"""
This section is about address matching. 
First I will drop out of state addresses
Second I will match the mailing address to the property address. 
       -For this, I can match either on full property address or just partial address. Full property address looks like this:
              1625 Grove Street, Charlottesville, VA
       -partial property address looks like this
              ,Charlottesville, VA
       For now I am choosing the partial property address. This is because full property address has typos and eliminates more results than necessary
"""

rockingham = rockingham[rockingham['mail_state2'] == 'VA']

######MAYBE DOUBLE CHECK THIS PART
print()
print('Dropping out of state mailing addresses')
print()

rockingham['full_mailing_address'] =  rockingham['mail_city'] + ', ' + rockingham['mail_state2']
rockingham['full_property_address'] = rockingham['scity'] + ', ' + rockingham['state2']
rockingham['address_match'] = np.where(rockingham['full_property_address'] == rockingham['full_mailing_address'], 'match', '')
rockingham = rockingham[rockingham['address_match'] == 'match']

print(f'There are {rockingham.shape[0]} parcels in Rockingham County')


### Remove properties that are on a north facing slope
"""
For this step I will read in the VA_North_Facing_Vector file and remove all parcels from Albemarle, Charlottesville, Culpeper 
that intersect with this layer. 
"""
north_facing_slopes = gpd.read_file('/Users/ep9k/Desktop/VirtueSolar/VA_North_Facing_Vector.gpkg')

print()
print('Removing parcels on north facing slopes')
print()

# Perform a left join
rockingham_result = gpd.sjoin(rockingham, north_facing_slopes, how='left', op='intersects')

# Filter rows where there is no intersection with north_facing_slopes
rockingham_no_intersection = rockingham_result[rockingham_result['DN'].isnull()]

print('After Spatial Filter')
print(f'Rockingham : {rockingham_no_intersection.shape[0]}')

print('Exporting results after spatial filter')
rockingham_no_intersection.to_csv('/Users/ep9k/Desktop/VirtueSolar/AfterSpatialFilter/Rockingham_Spatial.csv')


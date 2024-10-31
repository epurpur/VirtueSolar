

import pandas as pd
import geopandas as gpd
import numpy as np

### import county geopackage datasets
spotsylvania = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_spotsylvania.gpkg")

print(f'There are {spotsylvania.shape[0]} parcels in Spotsylvania County')


### look at zoning for each county/city
"""
Spotsylvania zoning values in "zoning_description" column

"""

#removing unwanted zoning from each county
print()
print('Removing parcels with unwanted zoning from each county')
print()

unwanted_zoning = ['AGRICULTURAL FORESTRAL | WATER | OPENSPACE',
 'SCENICROAD | RURAL',
 'MIXEDLIGHT | MIXEDCOMMCORE | OPENSPACE',
 'RURAL | OPENSPACE',
 'OPENSPACE | SCENICBYWAY | CIVILWARTRL',
 'INSTITUTIONAL | RURAL',
 'CIVILWARTRL | MIXEDLIGHT | RURAL',
 'MIXEDCOMMCORE | AGRICULTURAL FORESTRAL | WATER | OPENSPACE',
 'AGRICULTURAL FORESTRAL | RURAL | CIVILWARTRL | COMMERCIAL',
 'OPENSPACE | SCENICROAD | SCENICBYWAY',
 'SCENICBYWAY | OPENSPACE | SCENICROAD',
 'MIXEDCOMMCORE | MIXEDLIGHT | WATER | OPENSPACE',
 'AGRICULTURAL FORESTRAL | WATER | OPENSPACE | RURAL',
 'INSTITUTIONAL | AGRICULTURAL FORESTRAL | WATER | OPENSPACE',
 'RURAL | CIVILWARTRL | COMMERCIAL',
 'OPENSPACE | AGRICULTURAL FORESTRAL | RURAL',
 'MIXEDCOMMCORE | MIXEDLIGHT | RURAL',
 'CIVILWARTRL | RURAL',
 'AGRICULTURAL FORESTRAL | OPENSPACE | SCENICBYWAY',
 'SCENICROAD | COMMERCIAL | WATER | OPENSPACE',
 'INSTITUTIONAL | INSTITUTIONAL | AGRICULTURAL FORESTRAL',
 'MIXEDCOMMCORE | INSTITUTIONAL | RURAL',
 'OPENSPACE | MIXEDCOMMCORE | SCENICROAD',
 'SCENICBYWAY | COMMERCIAL | WATER | OPENSPACE',
 'AGRICULTURAL FORESTRAL | CIVILWARTRL | RURAL',
 'CIVILWARTRL | AGRICULTURAL FORESTRAL | RURAL',
 'OPENSPACE | MIXEDCOMMCORE | AGRICULTURAL FORESTRAL',
 'MIXEDLIGHT | AGRICULTURAL FORESTRAL | RURAL']

spotsylvania = spotsylvania[~spotsylvania['zoning_description'].isin(unwanted_zoning)]

print('After zoning filter...')
print(f'There are {spotsylvania.shape[0]} parcels in Spotsylvania County')


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


spotsylvania = spotsylvania[spotsylvania['mail_state2'] == 'VA']


print()
print('Dropping out of state mailing addresses')
print()

spotsylvania['full_mailing_address'] =  spotsylvania['mail_city'] + ', ' + spotsylvania['mail_state2']
spotsylvania['full_property_address'] = spotsylvania['scity'] + ', ' + spotsylvania['state2']
spotsylvania['address_match'] = np.where(spotsylvania['full_property_address'] == spotsylvania['full_mailing_address'], 'match', '')
spotsylvania = spotsylvania[spotsylvania['address_match'] == 'match']

print(f'There are {spotsylvania.shape[0]} parcels in Spotsylvania County')

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
spotsylvania_result = gpd.sjoin(spotsylvania, north_facing_slopes, how='left', op='intersects')

# Filter rows where there is no intersection with north_facing_slopes
spotsylvania_no_intersection = spotsylvania_result[spotsylvania_result['DN'].isnull()]


print('After Spatial Filter')
print(f'Spotsylvania : {spotsylvania_no_intersection.shape[0]}')

print('Exporting results after spatial filter')
spotsylvania_no_intersection.to_csv('/Users/ep9k/Desktop/VirtueSolar/AfterSpatialFilter/Spotsylvania_Spatial.csv')

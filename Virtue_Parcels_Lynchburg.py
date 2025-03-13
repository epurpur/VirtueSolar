

import pandas as pd
import geopandas as gpd
import numpy as np


### import county geopackage datasets
lynchburg = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_lynchburg.gpkg")

print(f'There are {lynchburg.shape[0]} parcels in Lynchburg')

#removing unwanted zoning from each county
print()
print('Removing parcels with unwanted zoning from each county')
print()

lynchburg_unwanted_zoning = [
 'I-2',
 'I-3',
 'IN-2',      
 'I-1',       
 'IN-1']

lynchburg = lynchburg[~lynchburg['zoning'].isin(lynchburg_unwanted_zoning)]

print('After zoning filter...')
print(f'There are {lynchburg.shape[0]} parcels in Lynchburg')

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

lynchburg = lynchburg[lynchburg['mail_state2'] == 'VA']

######MAYBE DOUBLE CHECK THIS PART
print()
print('Dropping out of state mailing addresses')
print()

lynchburg['full_mailing_address'] =  lynchburg['mail_city'] + ', ' + lynchburg['mail_state2']
lynchburg['full_property_address'] = lynchburg['scity'] + ', ' + lynchburg['state2']
lynchburg['address_match'] = np.where(lynchburg['full_property_address'] == lynchburg['full_mailing_address'], 'match', '')
lynchburg = lynchburg[lynchburg['address_match'] == 'match']


print(f'There are {lynchburg.shape[0]} parcels in Lynchburg')


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
lynchburg_result = gpd.sjoin(lynchburg, north_facing_slopes, how='left', op='intersects')

# Filter rows where there is no intersection with north_facing_slopes
lynchburg_no_intersection = lynchburg_result[lynchburg_result['DN'].isnull()]


print('After Spatial Filter')
print(f'Lynchburg : {lynchburg_no_intersection.shape[0]}')

print('Exporting results after spatial filter')
lynchburg_no_intersection.to_csv('/Users/ep9k/Desktop/VirtueSolar/AfterSpatialFilter/Lynchburg_Spatial.csv')



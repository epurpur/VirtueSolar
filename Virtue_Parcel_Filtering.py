

import pandas as pd
import geopandas as gpd
import numpy as np


### import county geopackage datasets
albemarle = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_albemarle.gpkg")
charlottesville = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_charlottesville.gpkg")
culpeper = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_culpeper_no_town.gpkg")

print(f'There are {albemarle.shape[0]} parcels in Albemarle County')
print(f'There are {charlottesville.shape[0]} parcels in Charlottesville City')
print(f'There are {culpeper.shape[0]} parcels in Culpeper County, minus city of Culpeper')


### look at zoning for each county/city
""" 
Albemarle zoning values in 'usedesc' column
None, 'Open', 'Residential -- Single-family (incl. modular homes)',
       'Industrial', 'Residential -- Townhouse', 'Commercial',
       'Unassigned', 'Residential -- Two family (e.g. duplex)', 'Forest',
       'Residential -- Mobile home',
       'Residential -- Single-family attached', 'Office', 'Semi-public',
       'Agricultural', 'Residential -- Condominium',
       'Residential -- Multi-family', 'Public',
       'Residential -- Group quarters (incl. fraternities, sororities)',
       'Parks', 'Water'

Charlottesville zoning values in 'zoning' column
'R-1', 'HW', 'PUD', 'R-1S', 'UMDH', 'M-I', 'B-1H', 'B-1', 'R-2',
       'CH', 'R-3', 'MLTP', 'B-2', 'R-1H', 'URB', 'IC', 'R-1SU', 'CDH',
       'ES', 'R-1U', 'R-3H', 'R-1UH', 'CC', 'R-2U', 'R-1SC', 'UHD', 'B-3',
       'MR', 'R-2H', 'R-1SUH', 'B-3H', 'CCH', 'UHDH', 'MLTPC', 'UMD',
       'ICH', 'R-1SH', 'HS', 'R-1C', 'B-2H', 'D', 'WMWH', 'DNH', 'B-1C',
       'DH', 'WMW', 'R-2C', 'WMEH', 'DN', 'MLTPH', 'WME', 'HSC', 'DNC',
       'R-2UH', 'CHH', 'WSH', 'SSH', 'DE', 'DEH', 'NCC', 'PUDH', 'R-1SHC',
       None

Culpeper zoning values in 'zoning' column
'RA', 'R1', 'CS', 'A1', 'R2', None, 'PUD', 'RR', 'CC', 'LI', 'PBD',
       'HI', 'R3', 'VC'

"""

#removing unwanted zoning from each county
print()
print('Removing parcels with unwanted zoning from each county')
print()
albemarle_unwanted_zoning = ['Industrial', 'Commercial', 'Unassigned', 'Residential -- Two family (e.g. duplex)', 'Forest', 'Office', 'Semi-public', 'Agricultural', 'Residential -- Condominium',
                             'Residential -- Multi-family', 'Public',
                             'Residential -- Group quarters (incl. fraternities, sororities)',
                             'Parks', 'Water']
albemarle = albemarle[~albemarle['usedesc'].isin(albemarle_unwanted_zoning)]

charlottesville_unwanted_zoning = ['HW', 'UMDH', 'M-I', 'B-1H', 'B-1', 'CH', 'MLTP', 'B-2', 'URB', 'IC', 'CDH', 'ES', 'CC', 'UHD', 'B-3', 'MR', 'B-3H', 'CCH', 'UHDH', 'MLTPC', 'UMD', 
                                   'ICH', 'HS', 'B-2H', 'D', 'WMWH', 'DNH', 'B-1C','DH', 'WMW', 'WMEH', 'DN', 'MLTPH', 'WME', 'HSC', 'DNC', None]
charlottesville = charlottesville[~charlottesville['zoning'].isin(charlottesville_unwanted_zoning)]

culpeper_unwanted_zoning = ['RA', 'CS', 'A1', 'None', 'RR', 'CC', 'LI', 'PBD', 'HI', 'VC']
culpeper = culpeper[~culpeper['zoning'].isin(culpeper_unwanted_zoning)]

print('After zoning filter...')
print(f'There are {albemarle.shape[0]} parcels in Albemarle County')
print(f'There are {charlottesville.shape[0]} parcels in Charlottesville City')
print(f'There are {culpeper.shape[0]} parcels in Culpeper County, minus city of Culpeper')



### Remove properties with less than certain property value
"""
Albemarle - all houses with improvval > $250k
Charlottesville - all houses with parval > $350k and townhomes > $400k.  There is actually no zoning information to indicate a townhome. 
Culpeper - all houses with improvval > $250k
"""
# albemarle = albemarle[((albemarle['usedesc'] == 'Residential -- Townhouse') & (albemarle['improvval'] > 400000))]
# albemarle = albemarle[albemarle['improvval'] > 250000]

albemarle = albemarle[(albemarle['improvval'] > 250000) | ((albemarle['usedesc'] == 'Residential -- Townhouse') & (albemarle['improvval'] > 400000))] #investigate this line some more
charlottesville = charlottesville[charlottesville['parval'] > 350000]
culpeper = culpeper[culpeper['improvval'] > 250000]

print()
print('Removing parcels with less than desired property value')
print()

print('After pricing filter...')
print(f'There are {albemarle.shape[0]} parcels in Albemarle County')
print(f'There are {charlottesville.shape[0]} parcels in Charlottesville City')
print(f'There are {culpeper.shape[0]} parcels in Culpeper County, minus city of Culpeper')



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

albemarle = albemarle[albemarle['mail_state2'] == 'VA']
charlottesville = charlottesville[charlottesville['mail_state2'] == 'VA']
culpeper = culpeper[culpeper['mail_state2'] == 'VA']

print()
print('Dropping out of state mailing addresses')
print()

# albemarle['full_mailing_address'] = albemarle['mailadd'] + ', ' + albemarle['mail_city'] + ', ' + albemarle['mail_state2']
# albemarle['full_property_address'] = albemarle['address'] + ', ' + albemarle['scity'] + ', ' + albemarle['state2']
# albemarle['address_match'] = np.where(albemarle['full_property_address'] == albemarle['full_mailing_address'], 'match', '')
# albemarle_test = albemarle[albemarle['address_match'] == 'match']

albemarle['full_mailing_address'] =  albemarle['mail_city'] + ', ' + albemarle['mail_state2']
albemarle['full_property_address'] = albemarle['scity'] + ', ' + albemarle['state2']
albemarle['address_match'] = np.where(albemarle['full_property_address'] == albemarle['full_mailing_address'], 'match', '')
albemarle = albemarle[albemarle['address_match'] == 'match']


# charlottesville['full_mailing_address'] = charlottesville['mailadd'] + ', ' + charlottesville['mail_city'] + ', ' + charlottesville['mail_state2']
# charlottesville['full_property_address'] = charlottesville['address'] + ', ' + charlottesville['scity'] + ', ' + charlottesville['state2']
# charlottesville['address_match'] = np.where(charlottesville['full_property_address'] == charlottesville['full_mailing_address'], 'match', '')
# charlottesville_test = charlottesville[charlottesville['address_match'] == 'match']

charlottesville['full_mailing_address'] = charlottesville['mail_city'] + ', ' + charlottesville['mail_state2']
charlottesville['full_property_address'] = charlottesville['scity'] + ', ' + charlottesville['state2']
charlottesville['address_match'] = np.where(charlottesville['full_property_address'] == charlottesville['full_mailing_address'], 'match', '')
charlottesville = charlottesville[charlottesville['address_match'] == 'match']

# culpeper['full_mailing_address'] = culpeper['mailadd'] + ', ' + culpeper['mail_city'] + ', ' + culpeper['mail_state2']
# culpeper['full_property_address'] = culpeper['address'] + ', ' + culpeper['scity'] + ', ' + culpeper['state2']
# culpeper['address_match'] = np.where(culpeper['full_property_address'] == culpeper['full_mailing_address'], 'match', '')
# culpeper_test = culpeper[culpeper['address_match'] == 'match']

culpeper['full_mailing_address'] = culpeper['mail_city'] + ', ' + culpeper['mail_state2']
culpeper['full_property_address'] = culpeper['scity'] + ', ' + culpeper['state2']
culpeper['address_match'] = np.where(culpeper['full_property_address'] == culpeper['full_mailing_address'], 'match', '')
culpeper = culpeper[culpeper['address_match'] == 'match']

print()
print('Matching addresses')
print()

print(f'There are {albemarle.shape[0]} parcels in Albemarle County')
print(f'There are {charlottesville.shape[0]} parcels in Charlottesville City')
print(f'There are {culpeper.shape[0]} parcels in Culpeper County, minus city of Culpeper')


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
albemarle_result = gpd.sjoin(albemarle, north_facing_slopes, how='left', op='intersects')
charlottesville_result = gpd.sjoin(charlottesville, north_facing_slopes, how='left', op='intersects')
culpeper_result = gpd.sjoin(culpeper, north_facing_slopes, how='left', op='intersects')


# Filter rows where there is no intersection with north_facing_slopes
albemarle_no_intersection = albemarle_result[albemarle_result['DN'].isnull()]
charlottesville_no_intersection = charlottesville_result[charlottesville_result['DN'].isnull()]
culpeper_no_intersection = culpeper_result[culpeper_result['DN'].isnull()]


print()
print('~~~~~~~~~Final Results~~~~~~~~~~')
print()
print('Before Spatial Filter')
print(f'Albemarle : {albemarle.shape[0]}')
print(f'Charlottesville : {charlottesville.shape[0]}')
print(f'Culpeper : {culpeper.shape[0]}')
print()
print()
print('After Spatial Filter')
print(f'Albemarle : {albemarle_no_intersection.shape[0]}')
print(f'Charlottesville : {charlottesville_no_intersection.shape[0]}')
print(f'Culpeper : {culpeper_no_intersection.shape[0]}')
print()
print()
print('Exporting results before and after spatial filter')

# export counties before spatial filter as csv
albemarle.to_csv('/Users/ep9k/Desktop/VirtueSolar/BeforeSpatialFilter/Albemarle_No_Spatial.csv')
charlottesville.to_csv('/Users/ep9k/Desktop/VirtueSolar/BeforeSpatialFilter/Charlottesville_No_Spatial.csv')
culpeper.to_csv('/Users/ep9k/Desktop/VirtueSolar/BeforeSpatialFilter/Culpeper_No_Spatial.csv')

# export counties before spatial filter as geopackage
albemarle.to_file('/Users/ep9k/Desktop/VirtueSolar/BeforeSpatialFilter/Albemarle_No_Spatial.gpkg', driver='GPKG')
charlottesville.to_file('/Users/ep9k/Desktop/VirtueSolar/BeforeSpatialFilter/Charlottesville_No_Spatial.gpkg', driver='GPKG')
culpeper.to_file('/Users/ep9k/Desktop/VirtueSolar/BeforeSpatialFilter/Culpeper_No_Spatial.gpkg', driver='GPKG')


# export counties after spatial filter as csv
albemarle_no_intersection.to_csv('/Users/ep9k/Desktop/VirtueSolar/AfterSpatialFilter/Albemarle_Spatial.csv')
charlottesville_no_intersection.to_csv('/Users/ep9k/Desktop/VirtueSolar/AfterSpatialFilter/Charlottesville_Spatial.csv')
culpeper_no_intersection.to_csv('/Users/ep9k/Desktop/VirtueSolar/AfterSpatialFilter/Culpeper_Spatial.csv')

# export counties after spatial filter as geopackage
albemarle.to_file('/Users/ep9k/Desktop/VirtueSolar/BeforeSpatialFilter/Albemarle_Spatial.gpkg', driver='GPKG')
charlottesville.to_csv('/Users/ep9k/Desktop/VirtueSolar/BeforeSpatialFilter/Charlottesville_No_Spatial.gpkg', driver='GPKG')
culpeper.to_csv('/Users/ep9k/Desktop/VirtueSolar/BeforeSpatialFilter/Culpeper_No_Spatial.gpkg', driver='GPKG')




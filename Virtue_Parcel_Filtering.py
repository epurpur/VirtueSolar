

import pandas as pd
import geopandas as gpd


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
albemarle = albemarle[(albemarle['improvval'] > 250000) | ((albemarle['usedesc'] == 'Residential -- Townhouse') & (albemarle['improvval'] > 400000))] #investigate this line some more
# albemarle = albemarle[albemarle['improvval'] > 250000]
charlottesville = charlottesville[charlottesville['parval'] > 350000]
culpeper = culpeper[culpeper['improvval'] > 250000]

print()
print('Removing parcels with less than desired property value')
print()

print('After pricing filter...')
print(f'There are {albemarle.shape[0]} parcels in Albemarle County')
print(f'There are {charlottesville.shape[0]} parcels in Charlottesville City')
print(f'There are {culpeper.shape[0]} parcels in Culpeper County, minus city of Culpeper')

####START HERE. did i make the not north facing slopes correctly?
### Remove properties that are on a north facing slope
# north_facing_slopes = gpd.read_file()







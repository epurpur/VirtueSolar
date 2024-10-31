

import pandas as pd
import geopandas as gpd
import numpy as np


### import county geopackage datasets
henrico = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_henrico.gpkg")

print(f'There are {henrico.shape[0]} parcels in Henrico County')


### look at zoning for each county/city
"""
Henrico zoning values in "usedesc" column

[
 'Vacant < 5 Acres',
 'Vacant Common Area (HOA)',
 'Vacant Residential',
 'Retail Strip',
 'Vacant Comm B1-B3',
 'Utilities',
 'Civic/Social/Fraternal',
 'Res - Imprv 5 - 10 Acres',
 'Motel/Hotel',
 'Res - Imprv < 5 Acres',
 'Vacant UMU/UMUC',
 'Warehouse',
 'Other Cultural',
 'Fast Food Restaurant',
 'Vacant 10 - 20 Acres',
 'Parks',
 'Railroad - Non Carrier',
 'Vacant 20 - 100 Acres',
 'Cemeteries',
 'Veterinary Hospital',
 'Vacant Industrial M1-M3,PMD',
 'Convenience Market',
 'Service Garage',
 'Office/Warehouse',
 'Communications',
 'Church & Synagogue',
 'Automotive/Retail Ctr',
 'Vacant 5 - 10 Acres',
 'Other Outdoor Rec',
 'HOA(Improved)',
 'Educational Facilities',
 'Res - Imprv > 100 Acres',
 'Shopping Center',
 'Indoor Recreation',
 'Cemetery Residential',
 'Mini Lube',
 'Golf Courses',
 "Other Gov't Buildings",
 'Computer Center',
 "Ind'l Flex Building",
 'Common Area (Non-HOA)',
 "Ind'l Manufacturing",
 'Fire Station',
 'Imprv Common Area (HOA)',
 'Bank',
 'Mini-Warehouse',
 'Vacant > 100 Acres',
 'Auto Dealership',
 'Group Care Home',
 'Hospitals/Health Care',
 'Movie Theatre',
 'Other Repair Services',
 'Post Office',
 'Construction Services',
 'Car Wash',
 'Railroad - Carrier',
 'Funeral Home',
 'Storage Garage',
 'Service Station',
 'Vacant Cultural Or Educ.',
 'Gas Station',
 'Parking Garage',
 'Coop',
 'Marinas',
 'Tool Shed',
 'Misc. Services',
 'Kennels',
 'Vacant Res (Sub. Wtrfrnt)',
 'Governmental Building',
 'Master Card',
 'Storage Hangar',
 None]
"""
#removing unwanted zoning from each county
print()
print('Removing parcels with unwanted zoning from each county')
print()

henrico_unwanted_zoning = [
 'Vacant < 5 Acres',
 'Vacant Common Area (HOA)',
 'Vacant Residential',
 'Retail Strip',
 'Vacant Comm B1-B3',
 'Utilities',
 'Civic/Social/Fraternal',
 'Res - Imprv 5 - 10 Acres',
 'Motel/Hotel',
 'Res - Imprv < 5 Acres',
 'Vacant UMU/UMUC',
 'Warehouse',
 'Other Cultural',
 'Fast Food Restaurant',
 'Vacant 10 - 20 Acres',
 'Parks',
 'Railroad - Non Carrier',
 'Vacant 20 - 100 Acres',
 'Cemeteries',
 'Veterinary Hospital',
 'Vacant Industrial M1-M3,PMD',
 'Convenience Market',
 'Service Garage',
 'Office/Warehouse',
 'Communications',
 'Church & Synagogue',
 'Automotive/Retail Ctr',
 'Vacant 5 - 10 Acres',
 'Other Outdoor Rec',
 'HOA(Improved)',
 'Educational Facilities',
 'Res - Imprv > 100 Acres',
 'Shopping Center',
 'Indoor Recreation',
 'Cemetery Residential',
 'Mini Lube',
 'Golf Courses',
 "Other Gov't Buildings",
 'Computer Center',
 "Ind'l Flex Building",
 'Common Area (Non-HOA)',
 "Ind'l Manufacturing",
 'Fire Station',
 'Imprv Common Area (HOA)',
 'Bank',
 'Mini-Warehouse',
 'Vacant > 100 Acres',
 'Auto Dealership',
 'Group Care Home',
 'Hospitals/Health Care',
 'Movie Theatre',
 'Other Repair Services',
 'Post Office',
 'Construction Services',
 'Car Wash',
 'Railroad - Carrier',
 'Funeral Home',
 'Storage Garage',
 'Service Station',
 'Vacant Cultural Or Educ.',
 'Gas Station',
 'Parking Garage',
 'Coop',
 'Marinas',
 'Tool Shed',
 'Misc. Services',
 'Kennels',
 'Vacant Res (Sub. Wtrfrnt)',
 'Governmental Building',
 'Master Card',
 'Storage Hangar',
 None]

henrico = henrico[~henrico['usedesc'].isin(henrico_unwanted_zoning)]

print('After zoning filter...')
print(f'There are {henrico.shape[0]} parcels in Henrico County')


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

henrico = henrico[henrico['mail_state2'] == 'VA']

######MAYBE DOUBLE CHECK THIS PART
print()
print('Dropping out of state mailing addresses')
print()


henrico['full_mailing_address'] =  henrico['mail_city'] + ', ' + henrico['mail_state2']
henrico['full_property_address'] = henrico['scity'] + ', ' + henrico['state2']
henrico['address_match'] = np.where(henrico['full_property_address'] == henrico['full_mailing_address'], 'match', '')
henrico = henrico[henrico['address_match'] == 'match']

print(f'There are {henrico.shape[0]} parcels in Henrico County')

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
henrico_result = gpd.sjoin(henrico, north_facing_slopes, how='left', op='intersects')

# Filter rows where there is no intersection with north_facing_slopes
henrico_no_intersection = henrico_result[henrico_result['DN'].isnull()]

print('After Spatial Filter')
print(f'Henrico : {henrico_no_intersection.shape[0]}')

print('Exporting results after spatial filter')
henrico_no_intersection.to_csv('/Users/ep9k/Desktop/VirtueSolar/AfterSpatialFilter/Henrico_Spatial.csv')


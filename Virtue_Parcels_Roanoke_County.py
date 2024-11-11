
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point


roanoke_county = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_roanoke.csv")


print(f'There are {roanoke_county.shape[0]} parcels in Roanoke County')

### look at the zoning for each city/county
"""
Roanoke county values in the zoning_description column

['Agricultural/Rural Preserve',
 'High Intensity Commercial District',
 'General Business District',
 'Low Density Residential',
 'Agricultural/Rural Low Density',
 'Planned Residential District',
 'Agricultural/ Residential',
 'Agricultural Village Center District',
 'Residential-Business District',
 'High Intensity Commercial District w/ Special Use',
 'Agricultural/Rural Preserve w/ Special Use',
 'Residential District',
 'High Intensity Commercial District w/ Conditions',
 'Medium Density Multi-family Residential',
 'Industrial (Heavy) District',
 'Medium Density Residential',
 'General Industrial District',
 'Explore Park District',
 'Agricultural/ Residential w/ Conditions',
 'Industrial (Heavy) District w/ Conditions',
 'Low Intensity Commercial District',
 'Low Density Residential w/ Special Use',
 'High Intensity Commercial District w/ Conditions & Special Use',
 'Medium Density Multi-family Residential w/ Conditions',
 'Medium Density Residential w/ Special Use',
 'Industrial (Light) District',
 'Central Business District',
 'Industrial (Light) District w/ Special Use',
 'Planned Technology District',
 'High Density Multi-family Residential w/ Conditions',
 'Public Open Space',
 'Agricultural/ Residential w/ Conditions & Special Use',
 'Agricultural/ Residential w/ Special Use',
 'Limited Industrial District',
 'Low Intensity Commercial District w/ Conditions',
 'Agricultural/Rural Low Density w/ Special Use',
 'Industrial (Light) District w/ Conditions',
 'Industrial (Heavy) District w/ Special Use',
 'Agricultural Village Center District w/ Conditions',
 'High Density Multi-family Residential',
 'Low Density Residential w/ Conditions',
 'General Business District w/ Conditions',
 'Residential Mixed Density District',
 'Agricultural/Rural Preserve w/ Conditions',
 'Agricultural/ Residential Manufactured Home',
 'Medium Density Residential w/ Conditions',
 'Agricultural Village Center District w/ Conditions & Special Use',
 'Agricultural Village Center District w/ Special Use',
 'Low Intensity Commercial District w/ Conditions & Special Use',
 'Medium Density Residential w/ Conditions & Special Use',
 'Mixed Use Development',
 'Low Density Residential w/ Conditions & Special Use',
 'Residential Single Family District',
 'Agricultural/Rural Low Density w/ Conditions',
 'Medium Density Multi-family Residential w/ Special Use',
 'Residential District w/ Conditions',
 'Industrial (Light) District w/ Conditions & Special Use',
 'Low Density Residential w/ Manufactured Home Overlay District',
 'Low Intensity Commercial District w/ Special Use',
 'General Industrial District w/ Conditions',
 '',
 'Planned Commercial District']

"""


#removing unwanted zoning from each county
print()
print('Removing parcels with unwanted zoning from each county')
print()

unwanted_zoning = ['Agricultural/Rural Preserve',
 'High Intensity Commercial District',
 'General Business District',
 'Agricultural/Rural Low Density',
 'Agricultural Village Center District',
 'High Intensity Commercial District w/ Special Use',
 'Agricultural/Rural Preserve w/ Special Use',
 'High Intensity Commercial District w/ Conditions',
 'Industrial (Heavy) District',
 'General Industrial District',
 'Explore Park District',
 'Industrial (Heavy) District w/ Conditions',
 'Low Intensity Commercial District',
 'High Intensity Commercial District w/ Conditions & Special Use',
 'Industrial (Light) District',
 'Central Business District',
 'Industrial (Light) District w/ Special Use',
 'Public Open Space',
 'Limited Industrial District',
 'Low Intensity Commercial District w/ Conditions',
 'Industrial (Light) District w/ Conditions',
 'Industrial (Heavy) District w/ Special Use',
 'Agricultural Village Center District w/ Conditions',
 'General Business District w/ Conditions',
 'Agricultural/Rural Preserve w/ Conditions',
 'Agricultural Village Center District w/ Conditions & Special Use',
 'Agricultural Village Center District w/ Special Use',
 'Low Intensity Commercial District w/ Conditions & Special Use',
 'Agricultural/Rural Low Density w/ Conditions',
 'Industrial (Light) District w/ Conditions & Special Use',
 'Low Intensity Commercial District w/ Special Use',
 'General Industrial District w/ Conditions',
 '',
 'Planned Commercial District']

roanoke_county = roanoke_county[~roanoke_county['zoning_description'].isin(unwanted_zoning)]

print('After zoning filter...')
print(f'There are {roanoke_county.shape[0]} parcels in Roanoke County')

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

roanoke_county = roanoke_county[roanoke_county['mail_state2'] == 'VA']

print()
print('Dropping out of state mailing addresses')
print()

roanoke_county['full_mailing_address'] =  roanoke_county['mail_city'] + ', ' + roanoke_county['mail_state2']
roanoke_county['full_property_address'] = roanoke_county['scity'] + ', ' + roanoke_county['state2']
roanoke_county['address_match'] = np.where(roanoke_county['full_property_address'] == roanoke_county['full_mailing_address'], 'match', '')
roanoke_county = roanoke_county[roanoke_county['address_match'] == 'match']

print(f'There are {roanoke_county.shape[0]} parcels in Roanoke County')


#convert to Geopackage from CSV file using lat/lon to make point
# Ensure 'lat' and 'lon' columns are numeric
roanoke_county['lat'] = pd.to_numeric(roanoke_county['lat'], errors='coerce')
roanoke_county['lon'] = pd.to_numeric(roanoke_county['lon'], errors='coerce')

# Check for any NaN values in lat/lon columns (in case some rows had non-numeric values)
if roanoke_county[['lat', 'lon']].isnull().any().any():
    print("Warning: There are some NaN values in lat/lon columns that will be skipped.")

# Drop rows with NaN values in 'lat' or 'lon' columns if needed
roanoke_county = roanoke_county.dropna(subset=['lat', 'lon'])


roanoke_county['geometry'] = roanoke_county.apply(lambda row: Point(row['lon'], row['lat']), axis=1)

gdf = gpd.GeoDataFrame(roanoke_county, geometry='geometry')
gdf.set_crs("EPSG:4326", inplace=True)


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
roanoke_county_result = gpd.sjoin(roanoke_county, north_facing_slopes, how='left', op='intersects')

# Filter rows where there is no intersection with north_facing_slopes
roanoke_county_no_intersection = roanoke_county_result[roanoke_county_result['DN'].isnull()]

print('After Spatial Filter')
print(f'There are {roanoke_county_no_intersection.shape[0]} parcels in Roanoke County')



#apply filter to remove parcels with parval < $250,000

print()
print('Removing parcels with < $250k parcel value')
print()

# Convert 'parval' to numeric, setting errors='coerce' to convert non-numeric values to NaN
roanoke_county_no_intersection['parval'] = pd.to_numeric(roanoke_county_no_intersection['parval'], errors='coerce')
# Drop rows where 'parval' is NaN (in case some rows couldn't be converted to a number)
roanoke_county_no_intersection = roanoke_county_no_intersection.dropna(subset=['parval'])
#apply filter to remove parcels with parval < $250,000
roanoke_county_no_intersection = roanoke_county_no_intersection[roanoke_county_no_intersection['parval'] >= 250000]


print('After Pricing Filter')
print(f'There are {roanoke_county_no_intersection.shape[0]} parcels in Roanoke County')


print('Exporting results after spatial filter')
roanoke_county_no_intersection.to_csv('/Users/ep9k/Desktop/VirtueSolar/AfterSpatialFilter/Roanoke_County_Spatial.csv')



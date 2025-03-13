import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point


### import county geopackage datasets
roanoke_city = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_roanoke_city.csv")

print(f'There are {roanoke_city.shape[0]} parcels in Roanoke City')

### look at the zoning for each city/county
"""
Roanoke city values in the usedesc column
['City',
 'MiscImp',
 'Religious',
 'Commercial Vacant',
 'Vacant Land',
 'State',
 'Commercial/Industrial',
 'Regional',
 'SingleFamily',
 'Other',
 'Multifamily',
 'Charitable',
 'SCC',
 'Res Condo Parent',
 'Family Duplex',
 'NonlivingArea',
 '',
 'Educational',
 'Federal',
 'Comm Condo Parent',
 'Commercial Condo']

"""

#removing unwanted zoning from each county
print()
print('Removing parcels with unwanted zoning from each county')
print()

unwanted_zoning = ['City',
 'MiscImp',
 'Religious',
 'Commercial Vacant',
 'State',
 'Commercial/Industrial',
 'Regional',
 'Other',
 'Charitable',
 'SCC',
 'NonlivingArea',
 '',
 'Educational',
 'Federal',
 'Comm Condo Parent',
 'Commercial Condo']

roanoke_city = roanoke_city[~roanoke_city['usedesc'].isin(unwanted_zoning)]


print('After zoning filter...')
print(f'There are {roanoke_city.shape[0]} parcels in Roanoke City')


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

roanoke_city = roanoke_city[roanoke_city['mail_state2'] == 'VA']

print()
print('Dropping out of state mailing addresses')
print()


roanoke_city['full_mailing_address'] =  roanoke_city['mail_city'] + ', ' + roanoke_city['mail_state2']
roanoke_city['full_property_address'] = roanoke_city['scity'] + ', ' + roanoke_city['state2']
roanoke_city['address_match'] = np.where(roanoke_city['full_property_address'] == roanoke_city['full_mailing_address'], 'match', '')
roanoke_city = roanoke_city[roanoke_city['address_match'] == 'match']

print(f'There are {roanoke_city.shape[0]} parcels in Roanoke City')



#convert to Geopackage from CSV file using lat/lon to make point
# Ensure 'lat' and 'lon' columns are numeric
roanoke_city['lat'] = pd.to_numeric(roanoke_city['lat'], errors='coerce')
roanoke_city['lon'] = pd.to_numeric(roanoke_city['lon'], errors='coerce')

# Check for any NaN values in lat/lon columns (in case some rows had non-numeric values)
if roanoke_city[['lat', 'lon']].isnull().any().any():
    print("Warning: There are some NaN values in lat/lon columns that will be skipped.")

# Drop rows with NaN values in 'lat' or 'lon' columns if needed
roanoke_city = roanoke_city.dropna(subset=['lat', 'lon'])


roanoke_city['geometry'] = roanoke_city.apply(lambda row: Point(row['lon'], row['lat']), axis=1)

gdf = gpd.GeoDataFrame(roanoke_city, geometry='geometry')
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
roanoke_city_result = gpd.sjoin(roanoke_city, north_facing_slopes, how='left', op='intersects')

# Filter rows where there is no intersection with north_facing_slopes
roanoke_city_no_intersection = roanoke_city_result[roanoke_city_result['DN'].isnull()]

print('After Spatial Filter')
print(f'There are {roanoke_city_no_intersection.shape[0]} parcels in Roanoke City')


#apply filter to remove parcels with parval < $250,000

print()
print('Removing parcels with < $250k parcel value')
print()

# Convert 'parval' to numeric, setting errors='coerce' to convert non-numeric values to NaN
roanoke_city_no_intersection['parval'] = pd.to_numeric(roanoke_city_no_intersection['parval'], errors='coerce')
# Drop rows where 'parval' is NaN (in case some rows couldn't be converted to a number)
roanoke_city_no_intersection = roanoke_city_no_intersection.dropna(subset=['parval'])
#apply filter to remove parcels with parval < $250,000
roanoke_city_no_intersection = roanoke_city_no_intersection[roanoke_city_no_intersection['parval'] >= 250000]





print('Exporting results after spatial filter')
roanoke_city_no_intersection.to_csv('/Users/ep9k/Desktop/VirtueSolar/AfterSpatialFilter/Roanoke_city_Spatial.csv')








import pandas as pd
import geopandas as gpd
import numpy as np

# import all cities/counties
albemarle = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_albemarle.gpkg")
charlottesville = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_charlottesville.gpkg")
culpeper = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_culpeper_no_town.gpkg")
lynchburg = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_lynchburg.gpkg")
henrico = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_henrico.gpkg")
spotsylvania = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_spotsylvania.gpkg")
rockingham = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_rockingham.gpkg")
roanoke_city = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_roanoke_city.csv")
roanoke_county = gpd.read_file("/Users/ep9k/Desktop/VirtueSolar/Regrid_Data/va_roanoke.csv")



#removing unwanted zoning from each county
print()
print('Removing parcels with unwanted zoning from each county')
print()

print('removing unwanted zoning from albemarle')
print()
albemarle_unwanted_zoning = ['Industrial', 'Commercial', 'Unassigned', 'Residential -- Two family (e.g. duplex)', 'Forest', 'Office', 'Semi-public', 'Agricultural', 'Residential -- Condominium',
                             'Residential -- Multi-family', 'Public',
                             'Residential -- Group quarters (incl. fraternities, sororities)',
                             'Parks', 'Water']
albemarle = albemarle[~albemarle['usedesc'].isin(albemarle_unwanted_zoning)]

print('removing unwanted zoning from charlottesville')
charlottesville_unwanted_zoning = ['HW', 'UMDH', 'M-I', 'B-1H', 'B-1', 'CH', 'MLTP', 'B-2', 'URB', 'IC', 'CDH', 'ES', 'CC', 'UHD', 'B-3', 'MR', 'B-3H', 'CCH', 'UHDH', 'MLTPC', 'UMD', 
                                   'ICH', 'HS', 'B-2H', 'D', 'WMWH', 'DNH', 'B-1C','DH', 'WMW', 'WMEH', 'DN', 'MLTPH', 'WME', 'HSC', 'DNC', None]
charlottesville = charlottesville[~charlottesville['zoning'].isin(charlottesville_unwanted_zoning)]


print('removing unwanted zoning from culpeper')
culpeper_unwanted_zoning = ['RA', 'CS', 'A1', 'None', 'RR', 'CC', 'LI', 'PBD', 'HI', 'VC']
culpeper = culpeper[~culpeper['zoning'].isin(culpeper_unwanted_zoning)]


print('removing unwanted zoning from lynchburg')
lynchburg_unwanted_zoning = [
    'Urban Commercial District',
    'Community Business District',
    'General Business District',
    'Limited Business District',
    'Light Industrial District',
    'Heavy Industrial District',
    'Conservation District',
    None,
    'Institutional District 2',
    'Restricted Industrial District',
    'Institutional District 1'
]
lynchburg = lynchburg[~lynchburg['zoning_description'].isin(lynchburg_unwanted_zoning)]


print('removing unwanted zoning from henrico')
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


print('removing unwanted zoning from spotsylvania')
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


print('removing unwanted zoning from rockingham')
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


print('removing unwanted zoning from roanoke city')
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


print('removing unwanted zoning from roanoke county')
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


# Filter dataframes for homes built within the last 30 years
albemarle = albemarle[albemarle['yearbuilt'] > 1996]
charlottesville = charlottesville[charlottesville['yearbuilt'] > 1996]
culpeper = culpeper[culpeper['yearbuilt'] > 1996]
henrico = henrico[henrico['yearbuilt'] > 1996]
spotsylvania = spotsylvania[spotsylvania['yearbuilt'] > 1996]
lynchburg = lynchburg[lynchburg['yearbuilt'] > 1996]
rockingham = rockingham[rockingham['yearbuilt'] > 1996]

# Convert to numeric (floats to handle potential NaNs)
roanoke_city['yearbuilt'] = pd.to_numeric(roanoke_city['yearbuilt'], errors='coerce')
roanoke_city = roanoke_city[roanoke_city['yearbuilt'] > 1996]

# Convert to numeric (floats to handle potential NaNs)
roanoke_county['yearbuilt'] = pd.to_numeric(roanoke_county['yearbuilt'], errors='coerce')
roanoke_county = roanoke_county[roanoke_county['yearbuilt'] > 1996]


# List of your DataFrames
newer_homes = [albemarle, charlottesville, culpeper, henrico, spotsylvania, lynchburg, rockingham, roanoke_city, roanoke_county]

# Stack them vertically
newer_homes = pd.concat(newer_homes, axis=0, join='inner', ignore_index=True)

#make full mailing address into one column
newer_homes['full_mail_address'] = (
    newer_homes['mailadd'] + ' ' + 
    newer_homes['mail_city'] + ', ' + 
    newer_homes['mail_state2'] + ' ' + 
    newer_homes['mail_zip']
)

newer_homes.to_csv('/Users/ep9k/Desktop/VirtueSolar/newer_homes.csv')




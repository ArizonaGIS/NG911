import arcpy

# Set the workspace and input feature classes
arcpy.env.workspace = r'C:\Locators\NG911 Data.gdb'

# Export feature classes from SDE database into the workspace, overwriting existing feature classes
arcpy.env.overwriteOutput = True
arcpy.FeatureClassToFeatureClass_conversion(r'C:\, 
                                            arcpy.env.workspace, 'AddressPoints')
arcpy.FeatureClassToFeatureClass_conversion(r', 
                                            arcpy.env.workspace, 'RoadCenterlines')

# Set the input feature classes for the address point, road centerline, and zip code polygon feature classes
address_points = 'AddressPoints'
road_centerlines = 'RoadCenterlines'
zipcodes = 'ZipCode_Boundary'

# Perform spatial intersect of AddressPointsV2 and ZipCode_Boundary
address_intersect = arcpy.Intersect_analysis([address_points, zipcodes], 'Address_Intersect')

# Perform spatial intersect of RoadCenterlinesV2 and ZipCode_Boundary
road_intersect = arcpy.Intersect_analysis([road_centerlines, zipcodes], 'Road_Intersect')

# Calculate fields in Address_Intersect
address_field_map = {
    'Post_Code': 'ZIP',
    'Post_Comm': 'PO_NAME'
}
with arcpy.da.UpdateCursor(address_intersect, ['Post_Code', 'Post_Comm', 'ZIP', 'PO_NAME']) as cursor:
    for row in cursor:
        if row[0] is None:
            row[0] = row[2]
        if row[1] is None:
            row[1] = row[3]
        cursor.updateRow(row)

# Calculate fields in Road_Intersect
road_field_map = {
    'PostCode_L': 'ZIP',
    'PostCode_R': 'ZIP',
    'PostComm_L': 'Post_Comm',
    'PostComm_R': 'Post_Comm'
}
with arcpy.da.UpdateCursor(road_intersect, ['PostCode_L', 'PostCode_R', 'PostComm_L', 'PostComm_R', 'ZIP', 'PO_NAME']) as cursor:
    for row in cursor:
        if row[0] in [None, '0', '00197', '00199'] and row[4] not in ['00197', '00199']:
            row[0] = row[4] if row[4] is not None else ''
        if row[1] in [None, '0', '00197', '00199'] and row[4] not in ['00197', '00199']:
            row[1] = row[4] if row[4] is not None else ''
        if row[2] is None and row[5] is not None:
            row[2] = row[5]
        if row[3] is None and row[5] is not None:
            row[3] = row[5]
        cursor.updateRow(row)

# Delete temporary fields in Address_Intersect and Road_Intersect
arcpy.DeleteField_management(address_intersect, ['ZIP', 'PO_NAME'])
arcpy.DeleteField_management(road_intersect, ['ZIP', 'PO_NAME'])

# Delete AddressPointsV2 and RoadCenterlinesV2 feature classes
arcpy.Delete_management(address_points)
arcpy.Delete_management(road_centerlines)

# Rename Address_Intersect and Road_Intersect feature classes to AddressPointsV2 and RoadCenterlinesV2
arcpy.Rename_management(address_intersect, address_points)
arcpy.Rename_management(road_intersect, road_centerlines)

# Create Address Locator
arcpy.geocoding.CreateLocator("USA", r"'C:\Locators\NG911 Data.gdb\AddressPoints' PointAddress", "'PointAddress.HOUSE_NUMBER AddressPoints.Add_Number';'PointAddress.STREET_PREFIX_DIR AddressPoints.St_PreDir';'PointAddress.STREET_PREFIX_TYPE AddressPoints.St_PreTyp';'PointAddress.STREET_NAME AddressPoints.St_Name';'PointAddress.STREET_SUFFIX_TYPE AddressPoints.St_PosTyp';'PointAddress.STREET_SUFFIX_DIR AddressPoints.St_PosDir';'PointAddress.SUB_ADDRESS_UNIT AddressPoints.Unit';'PointAddress.CITY AddressPoints.Post_Comm';'PointAddress.SUBREGION AddressPoints.County';'PointAddress.REGION_ABBR AddressPoints.State';'PointAddress.POSTAL AddressPoints.Post_Code';'PointAddress.COUNTRY AddressPoints.Country'", r"C:\Locators\Locators\SSAP_IncMunci.loc", "ENG", None, None, None, "GLOBAL_HIGH")

# Create Road Centerline Locator
arcpy.geocoding.CreateLocator("USA", r"'C:\Locators\NG911 Data.gdb\RoadCenterlines' StreetAddress", "'StreetAddress.FEATURE_ID RoadCenterlines.OBJECTID';'StreetAddress.HOUSE_NUMBER_FROM_LEFT RoadCenterlines.FromAddr_L';'StreetAddress.HOUSE_NUMBER_TO_LEFT RoadCenterlines.ToAddr_L';'StreetAddress.HOUSE_NUMBER_FROM_RIGHT RoadCenterlines.FromAddr_R';'StreetAddress.HOUSE_NUMBER_TO_RIGHT RoadCenterlines.ToAddr_R';'StreetAddress.PARITY_LEFT RoadCenterlines.Parity_L';'StreetAddress.PARITY_RIGHT RoadCenterlines.Parity_R';'StreetAddress.STREET_PREFIX_DIR RoadCenterlines.St_PreDir';'StreetAddress.STREET_PREFIX_TYPE RoadCenterlines.St_PreTyp';'StreetAddress.STREET_NAME RoadCenterlines.St_Name';'StreetAddress.STREET_SUFFIX_TYPE RoadCenterlines.St_PosTyp';'StreetAddress.STREET_SUFFIX_DIR RoadCenterlines.St_PosDir';'StreetAddress.FULL_STREET_NAME RoadCenterlines.ST_FULLNAME';'StreetAddress.CITY_LEFT RoadCenterlines.PostComm_L';'StreetAddress.CITY_RIGHT RoadCenterlines.PostComm_R';'StreetAddress.SUBREGION_LEFT RoadCenterlines.County_L';'StreetAddress.SUBREGION_RIGHT RoadCenterlines.County_R';'StreetAddress.REGION_ABBR_LEFT RoadCenterlines.State_L';'StreetAddress.REGION_RIGHT RoadCenterlines.State_R';'StreetAddress.POSTAL_LEFT RoadCenterlines.PostCode_L';'StreetAddress.POSTAL_RIGHT RoadCenterlines.PostCode_R';'StreetAddress.COUNTRY RoadCenterlines.Country_L'", r"C:\Locators\Locators\RCL_IncMunci.loc", "ENG", None, None, None, "GLOBAL_HIGH")

#Create composite locator using the address point, road centerline, and incorporated municpality point location
arcpy.geocoding.CreateCompositeAddressLocator(r"C:\Locators\Locators\SSAP_IncMunci.loc SSAP_IncMunci;C:\Locators\Locators\RCL_IncMunci.loc RCL_IncMunci;C:\Locators\Locators\City_IncMunci.loc City_IncMunci", r'Address "Address or Place" true true false 100 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,Address,0,0,C:\Locators\Locators\RCL_IncMunci.loc,Address,0,0,C:\Locators\Locators\City_IncMunci.loc,Address,0,0;Address2 "Address2" true true false 100 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,Address2,0,0,C:\Locators\Locators\RCL_IncMunci.loc,Address2,0,0,C:\Locators\Locators\City_IncMunci.loc,Address2,0,0;Address3 "Address3" true true false 100 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,Address3,0,0,C:\Locators\Locators\RCL_IncMunci.loc,Address3,0,0,C:\Locators\Locators\City_IncMunci.loc,Address3,0,0;Neighborhood "Neighborhood" true true false 50 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,Neighborhood,0,0,C:\Locators\Locators\RCL_IncMunci.loc,Neighborhood,0,0,C:\Locators\Locators\City_IncMunci.loc,Neighborhood,0,0;City "City" true true false 50 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,City,0,0,C:\Locators\Locators\RCL_IncMunci.loc,City,0,0,C:\Locators\Locators\City_IncMunci.loc,City,0,0;Subregion "County" true true false 50 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,Subregion,0,0,C:\Locators\Locators\RCL_IncMunci.loc,Subregion,0,0,C:\Locators\Locators\City_IncMunci.loc,Subregion,0,0;Region "State" true true false 50 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,Region,0,0,C:\Locators\Locators\RCL_IncMunci.loc,Region,0,0,C:\Locators\Locators\City_IncMunci.loc,Region,0,0;Postal "ZIP" true true false 20 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,Postal,0,0,C:\Locators\Locators\RCL_IncMunci.loc,Postal,0,0,C:\Locators\Locators\City_IncMunci.loc,Postal,0,0;PostalExt "ZIP4" true true false 20 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,PostalExt,0,0,C:\Locators\Locators\RCL_IncMunci.loc,PostalExt,0,0,C:\Locators\Locators\City_IncMunci.loc,PostalExt,0,0;CountryCode "Country" true true false 100 Text 0 0,First,#,C:\Locators\Locators\SSAP_IncMunci.loc,CountryCode,0,0,C:\Locators\Locators\RCL_IncMunci.loc,CountryCode,0,0,C:\Locators\Locators\City_IncMunci.loc,CountryCode,0,0', "SSAP_IncMunci #;RCL_IncMunci #;City_IncMunci #", r"C:\Locators\Locators\AZNG911_COMBO_LOCATOR.loc")

#Overwrite Composite Locator that is on ArcGIS Enterprise

from arcgis.gis import GIS
from arcgis.geocoding import create_locator_package

# Set the URL and credentials for your ArcGIS Enterprise/Portal instance
portal_url = 'https://portal.azgeo.az.gov/arcgis'
username = 'YOUR ARCGIS ENTERPRISE CONNECTION'
password = 'YOUR ARCGIS ENTERPRISE PASSWORD'

# Connect to the GIS and get the geocoding service
gis = GIS(portal_url, username, password)
geocoding_service = gis.content.search('url:https://server.azgeo.az.gov/arcgis/rest/services/geocoder/AZNG911_COMBO_LOCATOR/GeocodeServer', 'Geocoding Service')[0]

# Define the path to the locator package file and create the package
locator_path = r'C:\Locators\Locators\AZNG911_COMBO_LOCATOR.loc'
locator_package = create_locator_package(geocoding_service, locator_path)

# Overwrite the existing locator with the updated package file
geocoding_service.overwrite(locator_package)





import arcpy
import time

# Record the start time
start_time = time.time()

# Allow the script to overwrite any existing data
arcpy.env.overwriteOutput = True

# Set the workspace to the Enterprise Geodatabase
arcpy.env.workspace = r"C:\Dev\Dataset\DDTI_Export_20230412.gdb"

# Start an edit session
edit = arcpy.da.Editor(arcpy.env.workspace)
edit.startEditing(False, True)
edit.startOperation()

# Set the feature class to be modified
fc = r"AZ911_AddressPoints"

# Create a dictionary to match the prefixes to the correct "St_PreTyp" value
prefixes = {
    "Interstate": "Interstate",
    "Sr-": "State Route",
    #"US": "United States Highway",
    "BIA": "Bureau of Indian Affairs",
    "Usfs": "United States Forest Service Road",
    "Forest Road": "United States Forest Service Road",
    "Forest Service Rd": "United States Forest Service Road",
    "Fs Rd": "United States Forest Service Road",
    "Old Forest Service Road": "Old Forest Service Road",
    "Reservaton Rd": "Reservation Road",
    "Forest Service": "United States Forest Service Road",
    "Indian Route": "Indian Route",
    "Blm": "Bureau of Land Management",
    "FS ROAD": "United States Forest Service Road",
    "Us Highway": "United States Highway",
    "Us-": "United States Highway",
    "State Route": "State Route",
    "Old State Highway": "Old State Highway",
    "Old State Route": "Old State Route",
    "Old Highway": "Old Highway",
    "Sasabe Hy State Highway": "State Route",
    "Arizona State Route": "Arizona State Route",
    "Bia Route": "Bureau of Indian Affairs",
    "Bureau Of Indian Affairs Route": "Bureau of Indian Affairs",
    "Old Route": "Old Route",
    #"Route": "Route",
    "Nps Service": "National Park Service",
    "Foest Service": "United States Forest Service Road",
    "County Road": "County Road",
    "Old Us Highway": "Old United State Highway",
    "Old U.s.": "Old United State Highway",
    "State Highway": "State Highway",
    "Highway 181": "Highway",
    "Highway 186": "Highway",
    "Highway 90": "Highway",
    "Highway 92": "Highway",
    "Highway 60": "Highway",
    "Highway 80": "Highway",
    "Highway 82": "Highway",
    "Highway 83": "Highway",
    "Highway 85": "Highway",
    "Highway 86": "Highway",
    "Highway 191": "Highway",
    "Calle": "Calle",
    "Circulo ": "Circulo",
    "Avenida": "Avenida",
    "Via": "Via",
    "Camino": "Camino",
    "Paseo": "Paseo",
    #"Mc85": "Maricopa County",
}

# Use an update cursor to loop through the records in the feature class
with arcpy.da.UpdateCursor(fc, ["St_Name", "St_PreTyp"]) as cursor:
    for row in cursor:
        # Get the "St_Name" value
        st_name = row[0]
        
        if st_name is not None:
            update_required = True
            # Check if St_Name contains only the Spanish prefix
            if st_name.strip() in ["Calle", "Avenida", "Via", "Camino", "Paseo", "Interstate", "Old Highway", "Highway", "National Park Service"]:
                update_required = False  # No update required

            # If update is required, loop through the prefixes to find a match
            if update_required:
                for prefix, pretyp in prefixes.items():
                    if st_name.startswith(prefix):
                        # If additional characters are present, parse and update the fields
                        row[1] = pretyp
                        row[0] = st_name.replace(prefix, "").lstrip().replace("Highway", "").lstrip()
                        break
        else:
            row[1] = None
        
        # Update the record
        cursor.updateRow(row)

# Other parts of the code remain the same


# Stop the current operation
edit.stopOperation()

# Save the changes
edit.stopEditing(True)

# Record the end time
end_time = time.time()

# Calculate the total time in minutes
total_time = (end_time - start_time) / 60

print("Successfully updated parsing for feature class")
print("Total time taken: {:.2f} minutes".format(total_time))

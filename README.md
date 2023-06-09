# NG911
This repository contains a set of scripts that help clean and preprocess GIS data to meet the requirements of Next Generation 911 (NG911). The repository includes three main scripts that parse the street name field into the street pre-type field, define the parity of a road centerline segment based on the hundred range value, and create a composite geocoder based on NG911 address point and road centerline data, as well as a postal code polygon boundary.
Table of Contents
Getting Started
Scripts
Street Pre Type Parsing AZGeo.py
Update_Parity.py
create_composite_geocoder.py
Contributing
License
Getting Started
To use these scripts, clone this repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/NG911-GIS-Data-Cleaning.git
You will need Python installed on your system to run these scripts. You can download and install the latest version of Python from https://www.python.org/downloads/.

Additionally, ensure that you have installed any necessary Python libraries that these scripts require.

Scripts
Street Pre Type Parsing AZGeo
Street Pre Type Parsing AZGeo.py is a script that processes and parses the street name field into the street pre-type field. This helps standardize street names and abbreviations, as required by NG911.

Usage:

Copy code
python Pre Type Parsing AZGeo.py input_file output_file
Update_Parity
Update_Parity.py is a script that defines the parity of a road centerline segment based on the hundred range value. This ensures that address ranges are consistent and accurate.

Usage:

Copy code
python Update_Parity.py input_file output_file
create_composite_geocoder
create_composite_geocoder.py is a script that creates a composite geocoder based on NG911 address point and road centerline data, as well as a postal code polygon boundary. This allows for efficient and accurate geocoding for public safety applications.

Usage:

Copy code
python create_composite_geocoder.py address_point_data road_centerline_data postal_code_polygon_boundary output_directory
Contributing
Contributions are welcome! Please read our contributing guidelines to get started.

License
This project is licensed under the MIT License.

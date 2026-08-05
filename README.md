# laser_scaner
Python software for capturing a picture of laser projection and calculation it's coordinates.
To be updated by Raspberry pi 3b+ version.
It works in two modes:
1. Before calibration (and calibration itself) - default mode.
2. After calibration - workflow mode.

To operate in default mode use following english keys on keyboard:
q - finish program operations and close application
1 - start writing "data.txt" file (re)writes file with first coordinates set (x, y - from recognised positions, z - first constant from program code)
2 - continues writing "data.txt" file puts a second coordinates set (x, y - from recognised positions, z - first constant from program code) to the end of file
3 - continues writing "data.txt" file puts a third coordinates set (x, y - from recognised positions, z - first constant from program code) to the end of file
4 - continues writing "data.txt" file puts a fourth coordinates set (x, y - from recognised positions, z - first constant from program code) to the end of file
r - read a "data.txt" file and calculate internal calibration parameters. Since this moment program starts working in workflow mode

To operate in workflow mode use following english keys on keyboard:
q - finish program operations and close application
r - read a "data.txt" file and calculate internal calibration parameters
] - make a target circle to search bigger
[ - make a terget circle to search smaller
p - make a backbard rectangle bigger
o - make a backbard rectangle smaller

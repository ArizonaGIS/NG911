import arcpy
from arcpy import env
env.workspace = 'P:/eshreve/Export County Data/County Export/Cochise County/New File Geodatabase.gdb'
import time


fc = 'RoadCenterlines'

froml = 'FromAddr_L'
fromr = 'FromAddr_R'
tol = 'ToAddr_L'
tor = 'ToAddr_R'

def findParity(from_left, to_left, from_right, to_right):
    parity_l = None
    parity_r = None
    # Convert nulls to 0 and potential strings/floats to integers
    from_left = int(from_left) if from_left is not None else 0
    to_left = int(to_left) if to_left is not None else 0
    from_right = int(from_right) if from_right is not None else 0
    to_right = int(to_right) if to_right is not None else 0
    # find left parity
    if from_left != 0 or to_left != 0:
        diff_l = from_left - to_left
        if  diff_l % 2 == 0:
            if from_left % 2 == 0 and to_left % 2 == 0:
                parity_l = 'E'
            else:
                parity_l = 'O'
        else:
            parity_l = 'B'
    elif from_left == 0 and to_left == 0:
        parity_l = 'Z'
    # find right parity
    if from_right != 0 or from_left != 0:
        diff_r = from_right - to_right
        if  diff_r % 2 == 0:
            if from_right % 2 == 0 and to_right % 2 == 0:
                parity_r = 'E'
            else:
                parity_r = 'O'
        else:
            parity_r = 'B'
    elif from_right == 0 and to_right == 0:
        parity_r = 'Z'
    return (parity_l, parity_r)

arcpy.management.AddField(fc, "Parity_Left", "TEXT", None, None, 1, '', "NULLABLE", "NON_REQUIRED", '')

arcpy.management.AddField(fc, "Parity_Right", "TEXT", None, None, 1, '', "NULLABLE", "NON_REQUIRED", '')

with arcpy.da.UpdateCursor(fc, [froml, tol, fromr, tor, 'Parity_Left', 'Parity_Right']) as cursor:
    for row in cursor:
        p = findParity(*row[:4])
        row[4] = p[0]
        row[5] = p[1]
        cursor.updateRow(row)
    

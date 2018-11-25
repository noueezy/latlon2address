import sqlite3
import math
import sys


import PositionRefInfo as pri

dbpath = "addressLatLon.db"

def searchNearest(qlatDeg, qlonDeg):
    qlatRad = math.radians(qlatDeg)
    qlonRad = math.radians(qlonDeg)
    sinqLat = math.sin(qlatRad)
    sinqLon = math.sin(qlonRad)
    cosqLat = math.cos(qlatRad)
    cosqLon = math.cos(qlonRad)

    calcDistCos = "(sinLat * {0} + cosLat * {1} * (cosLon * {2} + sinLon * {3}))".format(sinqLat, cosqLat, cosqLon, sinqLon)

    selectCommand = \
    "select prefCode, prefName, cityCode, cityName, " \
    "sectionCode, sectionName, latitudeDeg, longitudeDeg, "\
    "originalCode, sectionClassCode, "\
    "{0} as distCos from AddLatLon "\
    "order by distCos DESC limit 5".format(calcDistCos)

    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    cur.execute(selectCommand)
    posRefInfoList = []
    distCosList = []

    for row in cur:
        posRefInfo = pri.PositionRefInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        posRefInfoList.append(posRefInfo)
        distCosList.append(row[10])

    cur.close()
    conn.close()

    distKm = 6371.0*math.acos(distCosList[0])

    return posRefInfoList[0], distKm
    
args = sys.argv

latDeg = float(args[1])
lonDeg = float(args[2])

posRefInfo, distKm = searchNearest(latDeg, lonDeg)

address = "{0} {1} {2}".format(posRefInfo.prefName, posRefInfo.cityName, posRefInfo.sectionName)
print(address)
print(distKm)
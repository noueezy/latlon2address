import sqlite3
import math
import sys
import time

import PositionRefInfo as pri

dbpath = "addressLatLon.db"

class AddressLatLonDB:

    def connect(self, path):
        self.conn = sqlite3.connect(dbpath)

    def disconnect(self):
        self.conn.close()

    def searchNearest(self, qlatDeg, qlonDeg):
        qlatRad = math.radians(qlatDeg)
        qlonRad = math.radians(qlonDeg)
        sinqLat = math.sin(qlatRad)
        sinqLon = math.sin(qlonRad)
        cosqLat = math.cos(qlatRad)
        cosqLon = math.cos(qlonRad)

        calcDistCos = "(sinLat * {0} + cosLat * {1} * (cosLon * {2} + sinLon * {3}))".format(sinqLat, cosqLat, cosqLon, sinqLon)

        degRange = 0.2

        selectCommand = \
        "select prefCode, prefName, cityCode, cityName, " \
        "sectionCode, sectionName, latitudeDeg, longitudeDeg, "\
        "originalCode, sectionClassCode, "\
        "{0} as distCos from AddLatLon "\
        "where latitudeDeg between {1} and {2} "\
        "and longitudeDeg between {3} and {4} "\
        "order by distCos DESC limit 5".format(calcDistCos, qlatDeg-degRange, qlatDeg+degRange, qlonDeg-degRange, qlonDeg+degRange)

        
        cur = self.conn.cursor()

        cur.execute(selectCommand)
        posRefInfoList = []
        distCosList = []

        for row in cur:
            posRefInfo = pri.PositionRefInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            posRefInfoList.append(posRefInfo)
            distCosList.append(row[10])

        cur.close()

        distKm = 6371.0*math.acos(distCosList[0])

        return posRefInfoList[0], distKm
    


if __name__ == '__main__':

    args = sys.argv
    if len(args) != 3:
        sys.exit()
    
    lat = float(args[1])
    lon = float(args[2])

    db = AddressLatLonDB()
    db.connect(dbpath)

    posRefInfo, distKm = db.searchNearest(lat, lon)

    db.disconnect()
    
    address = "{0} {1} {2}".format(posRefInfo.prefName, posRefInfo.cityName, posRefInfo.sectionName)
    print("address: {0}".format(address))
    print("distance(km): {0}".format(distKm))

    db.disconnect()
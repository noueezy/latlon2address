import sqlite3
import csv
import math
import glob
import re
import os

import PositionRefInfo as pri

dbpath = "addressLatLon.db"

class DBAddressLatLon:

    def CreateNewTable(self, dbpath):
        #都道府県コード
        #都道府県
        #市区町村コード
        #市区町村
        #大字町丁目コード
        #大字町丁目
        #緯度
        #軽度
        #原典資料コード
        #大字・字・丁目区分コード
        #sin(緯度)
        #sin(経度)
        #cos(緯度)
        #cos(経度)
        createTableCommand = \
        "create table if not exists AddLatLon ( " \
        "prefCode INTEGER, " \
        "prefName TEXT, " \
        "cityCode INTEGER, " \
        "cityName TEXT, " \
        "sectionCode INTEGER, " \
        "sectionName TEXT, " \
        "latitudeDeg REAL, " \
        "longitudeDeg REAL, " \
        "originalCode INTEGER, " \
        "sectionClassCode INTERGER, " \
        "sinLat REAL, " \
        "sinLon REAL, " \
        "cosLat REAL, " \
        "cosLon REAL )"

        conn = sqlite3.connect(dbpath)
        conn.execute(createTableCommand)
        conn.commit()
        conn.close()
    

    def __loadCSV(self, csvpath):
        posRefInfoList = []

        #csv読み込み
        with open(csvpath, 'r', encoding='Shift_JISx0213') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csv_reader)  # ヘッダ行をスキップ
            for row in csv_reader:
                if len(row) != 10:
                    continue
                posRefInfoElem = pri.PositionRefInfo(int(row[0]), row[1], int(row[2]), row[3], int(row[4]), row[5], float(row[6]), float(row[7]), int(row[8]), int(row[9]))
                posRefInfoList.append(posRefInfoElem)
        
        return posRefInfoList

    def __insertaddLatLon(self, ddbpath, AddLatLon):
        latRad = math.radians(AddLatLon.latitudeDeg)
        lonRad = math.radians(AddLatLon.longitudeDeg)
        insertCommand = "insert into AddLatLon values({0}, '{1}', {2}, '{3}', {4}, '{5}', {6}, {7}, {8}, {9}, {10}, '{11}', {12}, '{13}')".format(\
                AddLatLon.prefCode, \
                AddLatLon.prefName, \
                AddLatLon.cityCode, \
                AddLatLon.cityName, \
                AddLatLon.sectionCode, \
                AddLatLon.sectionName, \
                AddLatLon.latitudeDeg, \
                AddLatLon.longitudeDeg, \
                AddLatLon.originalCode, \
                AddLatLon.sectionClassCode, \
                math.sin(latRad), \
                math.sin(lonRad), \
                math.cos(latRad), \
                math.cos(lonRad))
        
        print(insertCommand)
        conn = sqlite3.connect(dbpath)
        conn.execute(insertCommand)
        conn.commit()
        conn.close()


    def AddCSV(self, dbpath, csvpath):
        addLatLonList = self.__loadCSV(csvpath)

        for elem in addLatLonList:
            self.__insertaddLatLon(dbpath, elem)



db = DBAddressLatLon()

db.CreateNewTable(dbpath)

files_csv = glob.glob('./data/*/*.csv')
files_csv.sort()

for f in files_csv:
    print(f)
    db.AddCSV(dbpath, f)

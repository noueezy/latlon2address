class PositionRefInfo:
#    def __init__(self, prefCode = 0, prefName = "", cityCode = 0, cityName = "", sectionCode = 0, sectionName = "", latitudeDeg = 0.0, longitudeDeg = 0.0, originalCode = 0, sectionClassCode = 0):
    def __init__(self, prefCode, prefName, cityCode, cityName, sectionCode, sectionName, latitudeDeg, longitudeDeg, originalCode, sectionClassCode):
        self.prefCode = prefCode
        self.prefName = prefName
        self.cityCode = cityCode
        self.cityName = cityName
        self.sectionCode = sectionCode
        self.sectionName = sectionName
        self.latitudeDeg = latitudeDeg
        self.longitudeDeg = longitudeDeg
        self.originalCode = originalCode
        self.sectionClassCode = sectionClassCode
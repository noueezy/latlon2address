#!/bin/bash

chromeDriverPath="XXXX"


python DownloadLocationReferenceInfo.py $chromeDriverPath
python Unzip.py
python ConvCsv2Sqlite.py
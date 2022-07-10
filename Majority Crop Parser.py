import matplotlib.pyplot as plt
import pandas as pd
from os import listdir
from os.path import isfile, join

csvs = [f for f in listdir("Majority Crop by County CSVs") if isfile(join("Majority Crop by County CSVs", f))]
print(csvs)
fileNames = []
for f in csvs:
    fileNames.append("Majority Crop by County CSVs/" + f)
print(fileNames)

cropNumber =input("Enter crop type number: ")
cropNumber = "VALUE_" + cropNumber

for county in fileNames:
    df = pd.read_csv(county)
    df = df[df["MAJORITY"] == cropNumber]
    totalArea = df["AREA"].sum()
    print(county)
    print(totalArea)


# ----------------------------------------------------------------------------------------------------------------------
# Name: THREE_Pixel_Data_Generator.py
# Created on: 3/15/2022
# Created by: Sean Hackenberg
# Description: This script contains the functions used with satellite(pixel) data
# Input:
#  - CSVs containing pixel based data for each field on a county by county basis
# ----------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import pandas as pd
from os import listdir
from os.path import isfile, join


# function used to get the total amount of acres planted for each year for each county at a certain threshold
def extract_pixel_data():
    # list of county csvs
    # county_csv = [r"County CSVs/BARBER20007.csv", r"County CSVs/COWLEY20035.csv", r"County CSVs/GRANT20067.csv",
    #               r"County CSVs/GRAY20069.csv", r"County CSVs/HARPER20077.csv", r"County CSVs/HARVEY20079.csv",
    #               r"County CSVs/HASKELL20081.csv", r"County CSVs/KINGMAN20095.csv",
    #               r"County CSVs/OTHER (COMBINED) COUNTIES.csv", r"County CSVs/PRATT20151.csv",
    #               r"County CSVs/SEDGEWICK20173.csv", r"County CSVs/SEWARD20175.csv", r"County CSVs/STEVENS20189.csv",
    #               r"County CSVs/SUMNER20191.csv"]
    csvs = [f for f in listdir("Corn County CSVs") if isfile(join("Corn County CSVs", f))]
    county_csv = []
    print(csvs)
    for f in csvs:
        county_csv.append("Corn County CSVs/" + f)
    print(county_csv)
    # Add to years to generate data for all years.
    # "AREA_2006", "AREA_2007", "AREA_2008", "AREA_2009", "AREA_2010", "AREA_2011", "AREA_2012",
    #             "AREA_2013", "AREA_2014", "AREA_2015",
    years = ["AREA_2016", "AREA_2017", "AREA_2018", "AREA_2019", "AREA_2020"]

    county_yearly_values = []

    # percentage of the field that needs to be covered by crop before the fields acreage is added to the total
    # acreage of the counties crop that is planted
    threshold = 0.0

    # main loop for getting the total amount of acres planted for each year for each county at a certain threshold
    for county in county_csv:
        df = pd.read_csv(county)
        list = []
        for year in years:
            df = df[df[year] != 0]
            df = df[df["Shape_Area"] != 0]
            df = df.assign(Percentage_Coverage=df[year]/df["Shape_Area"])
            mask = df['Percentage_Coverage'] >= threshold
            total = df.loc[mask, 'Shape_Area'].sum()
            total = total/4046.86

            # Old algorithm different results compared to new algorithm. Produced acreages over total county's acreage
            # total = 0
            # values = df[year].tolist()
            # shape_area = df["Shape_Area"].tolist()
            # fields_with_values = 0
            # for value in values:
            #     if value / shape_area[values.index(value)] >= threshold:
            #         total += (shape_area[values.index(value)] / 4046.86)
            #         fields_with_values += 1

            # Used for testing with new algorithm
            # fields_with_values = df.loc[mask, 'Shape_Area'].tolist()
            # print(len(fields_with_values))

            list.append(total)
        county_yearly_values.append(list)

    return county_csv, years, county_yearly_values


# function used for generating graphs containing the data from the function that is used to get the total amount of
# acres planted for each year for each county at a certain threshold
def plot_pixel_graphs(county_csv, years, pixel_yearly_values):
    # main loop for plotting
    for county in pixel_yearly_values:
        county_index = pixel_yearly_values.index(county)
        for dataByYear in county:
            x_axis = years
            y_axis = county
            plt.bar(x_axis, y_axis)
            plt.xticks(x_axis)
            plt.title(county_csv[county_index])
            plt.xlabel("Year")
            plt.ylabel("Value(ACRES)")
        plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# Name: THREE_Pixel_Threshold_Data.py
# Created on: 3/15/2022
# Created by: Sean Hackenberg
# Description: This script contains functions used for extracting data for each threshold from the satellite(pixel) data
# CSVs and plotting this data for each county
# Input:
#  - CSVs of each county (county_csv)
#  - Years being used to generate data (years)
# Output:
#  - List of values for each threshold for each county (yearly_value_per_threshold)
#  - List of survey data values for each county (survey_year_values)
#  - List of thresholds (1-100%) (thresholds)
#  - List of CSVs necessary for generating (necessary_csv)
#  - Graphs of pixel values per threshold versus survey data for each county (plot_pixel_threshold_data)
# ----------------------------------------------------------------------------------------------------------------------
import ONE_Corn_Survey_Data
import matplotlib.pyplot as plt
import pandas as pd


def extract_pixel_threshold_data3(county_csv, years, year):
    county_time_line, county_yearly_value, counties = ONE_Corn_Survey_Data.extract_survey_data()
    print("in extract pixel threshold data3")
    print(county_time_line)
    print(county_yearly_value)
    print(counties)

    # # switch for cotton
    # county_time_line, county_yearly_value, counties = ONE_Survey_Data_Generator.extract_survey_data()

    thresholds = []
    for i in range(101):
        percentage = i / 100
        thresholds.append(percentage)

    survey_year_values = []
    counties_with_data = []

    # this loop gets the survey values for a given year and appends that year's data to survey_year_values and appends
    # that county's name to counties_with_data, a list containing the county's that have data for that given year
    for county in county_time_line:
        for time in county:
            if time == int(year):
                survey_year_values.append(county_yearly_value[county_time_line.index(county)][county.index(time)])
                counties_with_data.append(counties[county_time_line.index(county)])

    print("The survey data values for " + year)
    print(survey_year_values)
    print("The counties this data belongs to")
    print(counties_with_data)

    # this loop gets the CSVs that match the counties that contain survey data for the given year
    necessary_csv = []
    necessary_county_dfs = []
    county_dfs = []
    for csv in county_csv:
        df = pd.read_csv(csv)
        df = df[df["AREA_" + year] != 0]
        county_dfs.append(df)
        for county in counties_with_data:
            if county in csv:
                necessary_county_dfs.append(df)
                necessary_csv.append(csv)

    print("The CSV files that match what counties contain survey data for the given year.")
    print(necessary_csv)

    yearly_value_per_threshold = []
    # The main loop that generates the total acreage of a county when a fields coverage meets/exceeds the threshold for
    # each percentage (1-100%)
    index = 0
    for df in necessary_county_dfs:
        print("Generating acreage at each threshold for " + necessary_csv[index])
        list = []
        for time in years:
            if time == ("AREA_" + year):
                values = df[time].tolist()
                shape_area = df["Shape_Area"].tolist()
                for percentage in thresholds:
                    total = 0
                    for value in values:
                        if value / shape_area[values.index(value)] >= percentage:
                            total += (shape_area[values.index(value)] / 4046.86)
                    list.append(total)
        yearly_value_per_threshold.append(list)
        index = index + 1
    # # change for cotton
    # print(yearly_value_per_threshold[necessary_csv.index(r"County CSVs/OTHER (COMBINED) COUNTIES.csv")])
    print(yearly_value_per_threshold[necessary_csv.index(r"Corn County CSVs/OTHER (COMBINED) COUNTIES.csv")])
    # this loop adds the acreage of fields not in necessary counties to other combined counties at each threshold
    print("Adding pixel data from counties with no survey data to OTHER_COMBINED_COUNTIES")
    for county in county_csv:
        if county not in necessary_csv:
            print("\tAdding pixel data from " + county + " to OTHER_COMBINED_COUNTIES")
            df = pd.read_csv(county)
            df = df[df["AREA_" + year] != 0]
            list = []
            for time in years:
                if time == ("AREA_" + year):
                    values = df[time].tolist()
                    shape_area = df["Shape_Area"].tolist()
                    for percentage in thresholds:
                        total = 0
                        for value in values:
                            if value / shape_area[values.index(value)] >= percentage:
                                total += (shape_area[values.index(value)] / 4046.86)
                        list.append(total)
            for i in range(101):
                # # change for cotton
                # yearly_value_per_threshold[necessary_csv.index(r"County CSVs/OTHER (COMBINED) COUNTIES.csv")][i] += \
                yearly_value_per_threshold[necessary_csv.index(r"Corn County CSVs/OTHER (COMBINED) COUNTIES.csv")][i] +=\
                list[i]

    # this list contains the normalized pixel values based on survey data for each county
    normalized_yearly_value_per_threshold = []
    for county in yearly_value_per_threshold:
        list = []
        for value in county:
            list.append(value / survey_year_values[yearly_value_per_threshold.index(county)])
        normalized_yearly_value_per_threshold.append(list)

    return normalized_yearly_value_per_threshold, survey_year_values, thresholds, necessary_csv, \
        yearly_value_per_threshold


def extract_pixel_threshold_data(county_csv, years, year):
    county_time_line, county_yearly_value, counties = ONE_Corn_Survey_Data.extract_survey_data()
    print(county_csv)
    # # switch for cotton
    # county_time_line, county_yearly_value, counties = ONE_Survey_Data_Generator.extract_survey_data()

    print("County_time_line")
    print(county_time_line)
    print("county_yearly_value")
    print(county_yearly_value)
    print("counties")
    print(counties)

    thresholds = []
    for i in range(101):
        percentage = i / 100
        thresholds.append(percentage)

    survey_year_values = []
    counties_with_data = []

    full_county = []
    for county in county_csv:
        full_county.append(county[17:-4])

    print(full_county)

    # this loop gets the survey values for a given year and appends that year's data to survey_year_values and appends
    # that county's name to counties_with_data, a list containing the county's that have data for that given year
    print(len(county_time_line))
    i=0
    while i < len(county_time_line):
        j=0
        while j < len(county_time_line[i]):
            if county_time_line[i][j] == int(year):
                survey_year_values.append(county_yearly_value[i][j])
                print(full_county[i])
                counties_with_data.append(full_county[i])
            j += 1
        i += 1

    # for county in county_time_line:
    #     if int(year) in county:
    #         index_of_year = county.index(int(year))
    #         survey_year_values.append(county_yearly_value[county_time_line.index(county)][index_of_year])
    #         counties_with_data.append(counties[county_time_line.index(county)])

    print(len(survey_year_values))
    print(len(counties_with_data))

    print("The survey data values for " + year)
    print(survey_year_values)
    print("The counties this data belongs to")
    print(counties_with_data)

    # this loop gets the CSVs that match the counties that contain survey data for the given year
    necessary_csv = []
    necessary_county_dfs = []
    county_dfs = []
    print(county_csv)
    for csv in county_csv:
        df = pd.read_csv(csv)
        df = df[df["AREA_" + year] != 0]
        county_dfs.append(df)

    for county in counties_with_data:
        new_csv = "Corn County CSVs/" + county + ".csv"
        df = pd.read_csv(new_csv)
        necessary_county_dfs.append(df)
        necessary_csv.append(new_csv)

    print("The CSV files that match what counties contain survey data for the given year.")
    print(necessary_csv)
    print(len(necessary_county_dfs))

    yearly_value_per_threshold = []
    # The main loop that generates the total acreage of a county when a fields coverage meets/exceeds the threshold for
    # each percentage (1-100%)
    index = 0
    for df in necessary_county_dfs:
        print("Generating acreage at each threshold for " + necessary_csv[index])
        list = []
        for time in years:
            if time == ("AREA_" + year):
                for percentage in thresholds:
                    total = 0
                    df = df[df["AREA_" + year] != 0]
                    df = df[df["Shape_Area"] != 0]
                    df = df.assign(Percentage_Coverage=df["AREA_" + year] / df["Shape_Area"])
                    mask = df['Percentage_Coverage'] >= percentage
                    total = df.loc[mask, 'Shape_Area'].sum()
                    total = total / 4046.86
                    list.append(total)
                if counties_with_data[index] == 'MCPHERSON20117':
                    print(list)
        yearly_value_per_threshold.append(list)
        index = index + 1

    # change for cotton
    # print(yearly_value_per_threshold[necessary_csv.index(r"County CSVs/OTHER (COMBINED) COUNTIES.csv")])
    print(yearly_value_per_threshold[necessary_csv.index(r"Corn County CSVs/OTHER (COMBINED) COUNTIES.csv")])

    # this loop adds the acreage of fields not in necessary counties to other combined counties at each threshold
    print("Adding pixel data from counties with no survey data to OTHER_COMBINED_COUNTIES")
    for county in county_csv:
        if county not in necessary_csv:
            print("\tAdding pixel data from " + county + " to OTHER_COMBINED_COUNTIES")
            df = pd.read_csv(county)
            df = df[df["AREA_" + year] != 0]
            list = []
            for time in years:
                if time == ("AREA_" + year):
                    for percentage in thresholds:
                        total = 0
                        df = df[df["AREA_" + year] != 0]
                        df = df[df["Shape_Area"] != 0]
                        df = df.assign(Percentage_Coverage=df["AREA_" + year] / df["Shape_Area"])
                        mask = df['Percentage_Coverage'] >= percentage
                        total = df.loc[mask, 'Shape_Area'].sum()
                        total = total / 4046.86
                        list.append(total)
            for i in range(101):
                # yearly_value_per_threshold[necessary_csv.index(r"County CSVs/OTHER (COMBINED) COUNTIES.csv")][i] +=\
                yearly_value_per_threshold[necessary_csv.index(r"Corn County CSVs/OTHER (COMBINED) COUNTIES.csv")][i] +=\
                    list[i]
    print(yearly_value_per_threshold[necessary_csv.index(r"Corn County CSVs/OTHER (COMBINED) COUNTIES.csv")])


    # this list contains the normalized pixel values based on survey data for each county
    normalized_yearly_value_per_threshold = []
    print(len(yearly_value_per_threshold))
    for county in yearly_value_per_threshold:
        list = []
        for value in county:
            list.append(value / survey_year_values[yearly_value_per_threshold.index(county)])
        normalized_yearly_value_per_threshold.append(list)

    print(len(survey_year_values))
    print(len(normalized_yearly_value_per_threshold))
    print(len(yearly_value_per_threshold))
    print(len(counties_with_data))
    # print(normalized_yearly_value_per_threshold[counties_with_data.index('SCOTT')])
    # print(counties_with_data.index('SCOTT'))
    # print(survey_year_values.index(102000))
    return normalized_yearly_value_per_threshold, survey_year_values, thresholds, necessary_csv, \
        yearly_value_per_threshold, counties_with_data


def generate_state_data(yearly_value_per_threshold, survey_year_values):
    # this list contains the total acreage at each threshold for the entire state.
    state_acreage_per_threshold = [0] * 101
    for county in yearly_value_per_threshold:
        for i in county:
            state_acreage_per_threshold[county.index(i)] += i
    # this value is the total survey value for the state
    state_survey = 0
    for value in survey_year_values:
        state_survey += value
    print("The total survey value for the state is " + str(state_survey))

    normalized_state_acreage_per_threshold = []
    for threshold in state_acreage_per_threshold:
        normalized_state_acreage_per_threshold.append(threshold / state_survey)
    print(normalized_state_acreage_per_threshold)
    return normalized_state_acreage_per_threshold


def plot_pixel_threshold_data(normalized_yearly_value_per_threshold, thresholds, necessary_csv):
    # this loop generates graphs showing the intersection of the survey data with the pixel data collected at each
    # threshold
    for percentages in normalized_yearly_value_per_threshold:
        x_axis = thresholds
        y_axis = percentages
        plt.plot(x_axis, y_axis, label=necessary_csv[normalized_yearly_value_per_threshold.index(percentages)])
        # plt.legend(loc="upper right")
        # plt.axhline(y=survey_year_values[yearly_value_per_threshold.index(percentages)], c='red')
        plt.axhline(y=1, c='black')
        plt.xticks(x_axis[0::10])
        plt.yscale('symlog')
        plt.title("Normalized Threshold Data vs Survey Data")
        plt.xlabel("% Thresholds")
        plt.ylabel("Normalized Value(Acres)")

    plt.show()
    #
    # x_axis = thresholds
    # y_axis = state_acreage_per_threshold
    # plt.plot(x_axis, y_axis)
    # # plt.axhline(y=survey_year_values[yearly_value_per_threshold.index(percentages)], c='red')
    # plt.axhline(y=state_survey, c='red')
    # plt.xticks(x_axis[0::10])
    # plt.title("State Threshold Data vs State Survey Data")
    # plt.xlabel("% Thresholds")
    # plt.ylabel("Acres")
    # plt.show()


def plot_pixel_threshold_data_state(state_yearly_value_per_threshold, thresholds):
    # this loop generates graphs showing the intersection of the survey data with the pixel data collected at each
    # threshold
    x_axis = thresholds
    y_axis = state_yearly_value_per_threshold
    plt.plot(x_axis, y_axis)
    # plt.legend(loc="upper right")
    # plt.axhline(y=survey_year_values[yearly_value_per_threshold.index(percentages)], c='red')
    plt.axhline(y=1, c='black')
    plt.xticks(x_axis[0::10])
    plt.yscale('symlog')
    plt.title("State thresholds vs State survey value")
    plt.xlabel("% Thresholds")
    plt.ylabel("Average State Value(Acres)")

    plt.show()
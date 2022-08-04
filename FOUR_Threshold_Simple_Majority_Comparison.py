import matplotlib.pyplot as plt
import pandas as pd
from os import listdir
from os.path import isfile, join


def get_simple_majority(valid_counties):
    csvs = [f for f in listdir("Majority Crop by County CSVs") if isfile(join("Majority Crop by County CSVs", f))]
    print(csvs)
    file_names = []
    for f in valid_counties:
        file_names.append("Majority Crop by County CSVs/" + f + ".csv")
    print(file_names)

    # crop_number =input("Enter crop type number: ")
    crop_number = "VALUE_" + "2"  # crop_number

    simple_majority_percentage = []
    for county in file_names:
        if county != 'Majority Crop by County CSVs/OTHER (COMBINED) COUNTIES.csv':
            df = pd.read_csv(county)
            df = df[df["MAJORITY_TYPE"] == crop_number]
            total_area = df["AREA"].sum()/4046.86
            simple_majority_percentage.append(total_area)
        else:
            total_area = 0
            for csv in csvs:
                if "Majority Crop by County CSVs/" + csv not in file_names:
                    df = pd.read_csv("Majority Crop by County CSVs/" + csv)
                    df = df[df["MAJORITY_TYPE"] == crop_number]
                    total_area += df["AREA"].sum() / 4046.86
            simple_majority_percentage.append(total_area)

    above_fifty_percentage = []
    for county in file_names:
        if county != 'Majority Crop by County CSVs/OTHER (COMBINED) COUNTIES.csv':
            df = pd.read_csv(county)
            df = df[df["MAJORITY_TYPE"] == crop_number]
            df = df[df["MAJORITY_PERCENTAGE"] >= .50]
            total_area = df["AREA"].sum()/4046.86
            above_fifty_percentage.append(total_area)
        else:
            total_area = 0
            for csv in csvs:
                if "Majority Crop by County CSVs/" + csv not in file_names:
                    df = pd.read_csv("Majority Crop by County CSVs/" + csv)
                    df = df[df["MAJORITY_TYPE"] == crop_number]
                    df = df[df["MAJORITY_PERCENTAGE"] >= .50]
                    total_area = df["AREA"].sum() / 4046.86
            above_fifty_percentage.append(total_area)

    print(simple_majority_percentage)
    print(above_fifty_percentage)
    return simple_majority_percentage, above_fifty_percentage


def get_closest_threshold_to_survey_value(yearly_values_per_threshold, values_for_each_county):
    closest_values = []
    for county in yearly_values_per_threshold:
        county_index = yearly_values_per_threshold.index(county)
        difference = 100000000
        closest_threshold_value = 0
        for threshold_value in county:
            threshold_index = county.index(threshold_value)
            if abs(threshold_value - values_for_each_county[county_index]) < difference:
                difference = abs(threshold_value - values_for_each_county[county_index])
                closest_threshold_value = threshold_value
        closest_values.append(closest_threshold_value)
    return closest_values


def plot_comparisons (counties_with_data, simple_majority_percentage, above_fifty_percent,
                      values_for_each_county, closest_threshold_values):
    # this loop generates graphs showing the intersection of the survey data with the pixel data collected at each
    # threshold
    # for value in values_for_each_county:
    #     i = values_for_each_county.index(value)
    #     simple_majority_percentage[i] = simple_majority_percentage[i]/value
    #     above_fifty_percent[i] = above_fifty_percent[i]/value
    x_axis = counties_with_data
    i=0
    for value in simple_majority_percentage:
        simple_majority_percentage[i] = value / values_for_each_county[i]
        closest_threshold_values[i] = closest_threshold_values[i]/values_for_each_county[i]
        i += 1
    plt.plot(x_axis, simple_majority_percentage, label="Simple Majority as Percentage of Survey Value")
    plt.plot(x_axis, closest_threshold_values, label="Threshold Value as Percentage of Survey Value")
    # plt.plot(x_axis, simple_majority_percentage, label="Normalized Simple Majority")
    # plt.plot(x_axis, above_fifty_percent, label="Normalized Coverage Above 50%")
    # plt.plot(x_axis, values_for_each_county, label="Survey Values")
    # plt.axhline(y=1, c='black', label="Normalized Survey Values")
    # plt.legend(loc="upper right")
    # plt.axhline(y=survey_year_values[yearly_value_per_threshold.index(percentages)], c='red')
    plt.axhline(y=sum(simple_majority_percentage)/len(simple_majority_percentage), c='black', label="Average SM Percentage")
    plt.axhline(y=sum(closest_threshold_values)/len(closest_threshold_values), c="green", label="Average Threshold Percentage")
    plt.xticks(x_axis)
    plt.title("Cotton 2020")
    plt.xticks(rotation=90)
    plt.xlabel("Counties")
    plt.ylabel("Simple Majority Value as a Percentage of Survey Values")
    plt.legend(loc="upper right")
    plt.show()

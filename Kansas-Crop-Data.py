# ----------------------------------------------------------------------------------------------------------------------
# Name: Cotton_In_Kansas.py
# Created on: 3/15/2022
# Created by: Sean Hackenberg
# Description: This script is a collection of the different functions being used to generate data and graphs for the
# Cotton in Kansas project.
#
# Input:
#  - User input on if a graph should be generated
#
# Output:
#  - Graphs generated from survey data on the acres of cotton planted per county
#  - Graphs generated from satellite(pixel) data on the acres of cotton planted per field
#  - Graphs generated comparing survey and satellite data based on the percentage of a field that needs to be identified
# as cotton before that fields total acreage is added to the counties total acres of cotton planted.
#
# ----------------------------------------------------------------------------------------------------------------------
import ONE_Corn_Survey_Data
import THREE_Pixel_Threshold_Data
import THREE_Pixel_Data_Generator
import FOUR_Field_Frequency_Distribution
import FOUR_Threshold_Simple_Majority_Comparison

# year = input("Type the year you would like to generate data for: ")
year = "2020"
generate_graphs = "0"

print("Generating survey based data...")
# countyTimeLine, county_yearly_value, counties = ONE_Survey_Data_Generator.extract_survey_data()
years_for_each_county, values_for_each_county, counties = ONE_Corn_Survey_Data.extract_survey_data()
# ONE_Corn_Survey_Data.generate_survey_table(years_for_each_county, values_for_each_county, counties)
# generate_graphs = input("Type 1 to generate graphs for survey data: ")

if generate_graphs == "1":
    # ONE_Survey_Data_Generator.plot_survey_graphs(countyTimeLine, county_yearly_value, counties)
    ONE_Corn_Survey_Data.plot_survey_graphs(years_for_each_county, values_for_each_county, counties)

print("Generating pixel based data with a threshold of 0....")
county_csv, years, pixel_yearly_values = THREE_Pixel_Data_Generator.extract_pixel_data()

# generate_graphs = input("Type 1 to generate graphs for pixel data: ")

if generate_graphs == "1":
    THREE_Pixel_Data_Generator.plot_pixel_graphs(county_csv, years, pixel_yearly_values)

print("Generating pixel threshold data...")
normalized_yearly_value_per_threshold, survey_year_values, thresholds, necessary_csv, yearly_value_per_threshold, \
    counties_with_data = THREE_Pixel_Threshold_Data.extract_pixel_threshold_data(county_csv, years, year)

print("Generating state threshold data...")
normalized_state_values = THREE_Pixel_Threshold_Data.generate_state_data(yearly_value_per_threshold, survey_year_values)

# generate_graphs = input("Type 1 to generate graphs for pixel threshold data: ")

if generate_graphs == "1":
    THREE_Pixel_Threshold_Data.plot_pixel_threshold_data(
        normalized_yearly_value_per_threshold, thresholds, necessary_csv)
    THREE_Pixel_Threshold_Data.plot_pixel_threshold_data_state(
        normalized_state_values, thresholds)

county_distributions = FOUR_Field_Frequency_Distribution.data_generator(thresholds, county_csv, year)
# generate_graphs = input("Type 1 to generate graphs for frequency distribution data: ")

if generate_graphs == "1":
   FOUR_Field_Frequency_Distribution.plot_counties(thresholds, county_distributions, year, counties)

closest_threshold_values = FOUR_Threshold_Simple_Majority_Comparison.get_closest_threshold_to_survey_value \
    (yearly_value_per_threshold, survey_year_values)

simple_majority_percentage, above_fifty_percent = \
    FOUR_Threshold_Simple_Majority_Comparison.get_simple_majority(counties_with_data)

FOUR_Threshold_Simple_Majority_Comparison.plot_comparisons(counties_with_data, \
                                                           simple_majority_percentage, above_fifty_percent, survey_year_values, closest_threshold_values)

# FOUR_Table_Generator.table_generator(necessary_csv, normalized_yearly_value_per_threshold, thresholds, normalized_state_values)
# FOUR_Table_Generator.county_distribution(counties, thresholds,county_distributions)

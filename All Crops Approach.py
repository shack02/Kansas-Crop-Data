from Research_Methods import get_survey_df, get_crop_identifiers, get_field_df, get_county_code, get_counties_with_survey_data, get_crop_identifiers
import pandas as pd

survey_file = "Other Crop Data (Corn, Cotton, Soybeans, Sorghum,  and Wheat).csv"
county_information_file = "Cotton_County_Kansas.csv"
year = 2020
survey_df = get_survey_df(survey_file, year)
crop_types = survey_df["Commodity"].unique().tolist()
field_file = "CLU_CDL_KS_2020_UNION.txt"
majority_file = "CLU_CDL_2020_MajorityCrop.txt"
crop_id_file = "CDL_2020_Count.txt"
crop_ids = get_crop_identifiers(crop_id_file, crop_types)
field_df = get_field_df(field_file, majority_file)

counties = survey_df["County"].unique().tolist()
print(len(counties))
county_codes = get_county_code(county_information_file, counties)
print(len(county_codes))
county_dfs = []
# for code in county_codes:
county_dfs.append(field_df[field_df["FIPSSTCO"] == str(county_codes[0])])

#First county is 20009 or
def get_survey_values_for_county(survey_df, counties):
    crops_for_county = survey_df[survey_df["County"] == counties[0]]["Commodity"].tolist()
    survey_values_for_county = survey_df[survey_df["County"] == counties[0]]["Value"].tolist()
    i = 0
    for value in survey_values_for_county:
        survey_values_for_county[i] = int(value.replace(",", ""))
        i += 1
    return crops_for_county, survey_values_for_county

crops_for_each_county = []
survey_values_for_each_county = []
crop_types, survey_values = get_survey_values_for_county(survey_df, counties)
crops_for_each_county.append(crop_types)
survey_values_for_each_county.append(survey_values)
print(crops_for_each_county[0])
print(survey_values_for_each_county[0])




crop_ids = get_crop_identifiers(crop_id_file, crops_for_each_county[0])
print(crop_ids)

threshold = 1.00
index = 0
current_df = county_dfs[0]
# This loop goes through each county's crop survey values and allocates fields until the survey values are reached
for survey_values in survey_values_for_each_county:
    threshold = 1.00
    final_thresholds_for_each_crop_in_county = [0]*len(survey_values)
    allocated_crop_values = [0]*len(survey_values)
    allocated_county_field_dfs = [pd.DataFrame()]*len(survey_values)
    while(threshold > 0):
        crop_index = 0
        for value in survey_values:
            if(value > allocated_crop_values[crop_index]):
                allocated_county_field_dfs[crop_index] = current_df[current_df[crops_for_each_county[0][crop_index] + "%"] >= threshold]
                print(crops_for_each_county[0][crop_index])
                print(value)
                allocated_crop_values[crop_index] = allocated_county_field_dfs[crop_index]["AREA"].sum() / 4046.86
                print(allocated_crop_values[crop_index])
                if(value > allocated_crop_values[crop_index]):
                    final_thresholds_for_each_crop_in_county[crop_index] = threshold
            crop_index += 1
            county_dfs[0]
        threshold -= .01
        print(threshold)
    print("Final Statistics - Survey Values, Allocated Values, Allocate Values / Survey Values, Final thresholds for each crop in county")
    print(survey_values)
    print(allocated_crop_values)
    percent_of_survey_values = [0]*len(survey_values)
    j = 0
    for value in survey_values:
        percent_of_survey_values[j] = allocated_crop_values[j]/value
        j += 1
    print(percent_of_survey_values)
    print(final_thresholds_for_each_crop_in_county)
    index += 1


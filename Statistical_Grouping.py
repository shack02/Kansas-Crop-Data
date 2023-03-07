from Research_Methods import get_survey_df, get_crop_identifiers, get_field_df_without_double_crops, get_county_code, \
    get_counties_with_survey_data, get_crop_identifiers, get_county_dfs
import pandas as pd
import numpy as np
import matplotlib as plt

survey_file = "Other Crop Data (Corn, Cotton, Soybeans, Sorghum,  and Wheat).csv"
county_information_file = "Cotton_County_Kansas.csv"
year = 2020
survey_df = get_survey_df(survey_file, year)
crop_types = survey_df["Commodity"].unique().tolist()
field_file = "CLU_CDL_KS_2020_UNION.txt"
majority_file = "CLU_CDL_2020_MajorityCrop.txt"
crop_id_file = "CDL_2020_Count.txt"
crop_ids = get_crop_identifiers(crop_id_file, crop_types)
field_df = get_field_df_without_double_crops(field_file, majority_file)

counties = survey_df["County"].unique().tolist()
print(len(counties))
county_codes = get_county_code(county_information_file, counties)
print(len(county_codes))
county_dfs = []
# for code in county_codes:
for code in county_codes:
    county_dfs.append(field_df[field_df["FIPSSTCO"] == str(code)])

i =0
for county in county_dfs:
    plt.pyplot.scatter(county["NumberCropsPresent"].tolist(), county["Skewness"].tolist(),  marker=".", alpha=0.1, s=2)
    # fig=plt.pyplot.figure(figsize = (16,9))
    # ax = plt.pyplot.axes(projection="3d")
    # ax.grid(b = True, color = "grey", linestyle = '-.', linewidth=0.3, alpha = 0.2)
    # my_cmap = plt.pyplot.get_cmap('hsv')
    # sctt = ax.scatter3D(county["Skewness"].tolist(), county["NormalizedStandardDeviation"].tolist(), county["NumberCropsPresent"].tolist(),
    #                     alpha = 0.8,
    #                     c= (county["Skewness"].tolist() + county["NormalizedStandardDeviation"].tolist() + county["NumberCropsPresent"].tolist()),
    #                     cmap=my_cmap,
    #                     marker= '.')
    plt.pyplot.xlabel("Number of Crops Present in Field")
    plt.pyplot.ylabel("Skewness of Field")
    # plt.pyplot.zlabel("Number of Crop in Field")
    plt.pyplot.title("CountyID:" + str(county_codes[i]))

    plt.pyplot.show()
    i += 1
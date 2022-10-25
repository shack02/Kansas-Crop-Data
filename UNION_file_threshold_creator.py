import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
# This file contains methods to create threshold data from the union dataset and compare it to the survey values.


# This function uses the survey_file and year given to create a dataframe containing survey data.
def get_survey_df(survey_file, year):
    survey_df = pd.read_csv(survey_file)
    survey_df = survey_df[survey_df["Year"] == int(year)]
    survey_df = survey_df.loc[survey_df["Data Item"].str.contains("ACRES PLANTED", case=False)]
    return survey_df


# This function
def get_county_code(county_information_file, counties):
    df = pd.read_csv(county_information_file)
    county_codes = []
    for county in counties:
        if county != "OTHER (COMBINED) COUNTIES":
            row = df[df["COUNTY"].str.upper() == county.upper()]
            county_codes.append(row.iloc[0]["FIPSSTCO"])
    return county_codes


# This function uses the field_file given to create a dataframe containing information on the crops
def get_field_df(field_file,majority_file):
    chunk_list = []
    majority_list = []
    for df_chunk in pd.read_csv(majority_file, chunksize=10000):
        majority_list.append(df_chunk)
    i=0
    for df_chunk in pd.read_csv(field_file, chunksize=10000):
        df_chunk["AREA"] = majority_list[i]["AREA"]
        # Corn
        df_chunk["VALUE_1"] = df_chunk["VALUE_1"] + df_chunk["VALUE_225"] + df_chunk["VALUE_226"] + df_chunk["VALUE_228"]
        # Sorghum
        df_chunk["VALUE_4"] = df_chunk["VALUE_4"] + df_chunk["VALUE_236"]
        # Soybeans
        df_chunk["VALUE_5"] = df_chunk["VALUE_5"] + df_chunk["VALUE_26"] + df_chunk["VALUE_240"] + df_chunk["VALUE_254"]
        # Wheat
        df_chunk["VALUE_24"] = df_chunk["VALUE_24"] + df_chunk["VALUE_26"] + df_chunk["VALUE_225"] + df_chunk[
            "VALUE_236"] + df_chunk["VALUE_238"]
        # Cotton
        df_chunk["VALUE_2"] = df_chunk["VALUE_2"] + df_chunk["VALUE_238"]
        df_chunk["FIPSSTCO"] = df_chunk["SCTFS"].astype(str).str.slice(0, 5)
        chunk_list.append(df_chunk)
        i += 1
    field_df = pd.concat(chunk_list)
    return field_df


# This function finds the percentage coverage of the crop given in each field
def get_crop_threshold_df(field_df, crop_value):
    crop_df = field_df
    crop_df["PERCENT COVERAGE"] = crop_df[crop_value] / crop_df["AREA"]
    crop_df['PERCENT COVERAGE'] = crop_df['PERCENT COVERAGE'].astype(float)
    crop_df = crop_df[crop_df["PERCENT COVERAGE"] != 0]
    print(crop_df)
    return crop_df


# This function gets the numerical IDs belonging to each crop type
def get_crop_identifiers(crop_id_file, crop_types):
    crop_id_df = pd.read_csv(crop_id_file)
    crop_ids = []
    for crop in crop_types:
        if crop != "WHEAT":
            row = crop_id_df[crop_id_df["CLASS_NAME"].str.upper() == crop]
            crop_ids.append("VALUE_" + str(row.iloc[0]["VALUE"]))
        else:
            row = crop_id_df[crop_id_df["CLASS_NAME"].str.upper() == "WINTER WHEAT"]
            crop_ids.append("VALUE_" + str(row.iloc[0]["VALUE"]))
    return crop_ids


# This function returns a dataframe containing the given crops survey values
def get_counties_with_survey_data(survey_df, crop):
    survey_crop_df = survey_df[survey_df["Commodity"] == crop]
    return survey_crop_df


# This function returns dataframes containing a single counties fields
def get_county_dfs(df, counties_for_each_crop):
    county_dfs = []
    crop_df = df
    for county_id in counties_for_each_crop:
        county_df = crop_df[crop_df["FIPSSTCO"] == str(county_id)]
        county_dfs.append(county_df)
    print(len(county_dfs))
    all_ids = crop_df['FIPSSTCO'].unique().tolist()

    necessary_counties = [str(x) for x in counties_for_each_crop]
    county_df = crop_df
    print(all_ids)
    print(necessary_counties)
    print(len(county_df))
    for id in all_ids:
        if id in necessary_counties:
            county_df = county_df[county_df["FIPSSTCO"] != str(id)]
    print("Crop df length after cut ************************************************************")
    print(len(county_df))
    county_dfs.append(county_df)
    print(len(county_dfs))
    return county_dfs


# This function generates threshold data for each county by crop
def get_threshold_crop_data(thresholds, county_dfs_by_crop, crop_ids, county_names_for_each_crop):
    threshold_crop_data = []
    for crop_dfs in county_dfs_by_crop:
        crop_threshold_values_by_county = []
        for county_df in crop_dfs:
            threshold_values_for_county = []
            for percent in thresholds:
                threshold_df = county_df[county_df["PERCENT COVERAGE"].astype(float) >= percent]
                threshold_value = threshold_df["AREA"].sum() / 4046.86
                threshold_values_for_county.append(threshold_value)
            crop_threshold_values_by_county.append(threshold_values_for_county)
        threshold_crop_data.append(crop_threshold_values_by_county)
    return threshold_crop_data


# This function creates dataframes containing threshold crop data for each crop
def create_threshold_dfs(threshold_crop_data, crop_ids, county_names_for_each_crop, thresholds):
    i = 0
    threshold_crop_dfs = []
    for crop_threshold_values_by_county in threshold_crop_data:
        crop_df = pd.DataFrame(index =thresholds, columns =[county_names_for_each_crop[i]])
        j = 0
        for county in county_names_for_each_crop[i]:
            crop_df[county] = crop_threshold_values_by_county[j]
            j += 1
        i += 1
        threshold_crop_dfs.append(crop_df)
    return threshold_crop_dfs


# This function normalizes the threshold crop values to their respective county's survey values
def normalize_threshold_values(survey_values_by_crop_dfs, threshold_crop_dfs):
    i = 0
    normalized_threshold_dfs = []
    for threshold_df in threshold_crop_dfs:
        df = threshold_df
        survey_df = survey_values_by_crop_dfs[i]
        counties = survey_df["County"].tolist()
        for county in counties:
            row = survey_df.loc[survey_df["County"] == county]
            value = int(float(row["Value"].iat[0].replace(',', '')))
            df[county] = df[county].astype(int) / value
        i += 1
        normalized_threshold_dfs.append(df)
    return normalized_threshold_dfs


# This function graphs the normalized threshold values
def graph_normalized_threshold_values(normalized_thresholds_df, crop_types, year, thresholds):
    i = 0
    for df in normalized_thresholds_df:
        crop = crop_types[i]
        title = "Normalized Threshold Values, " + crop + " " + str(year)
        plt.yscale('symlog')
        plt.axhline(y=1, c='black')
        plt.xticks(thresholds[0::10])
        plt.xlabel("Field Percentage Required")
        plt.ylabel("Normalized Threshold Values vs Survey Values")
        plt.title(title)
        for column in df:
            plt.plot(thresholds, df[column].tolist())
        plt.show()
        i += 1

def create_threshold_tables(normalized_thresholds_dfs, crop_types, county_distributions):
    index = 0
    for df in normalized_thresholds_dfs:
        print(df)
        df.to_csv(r"C:\Users\Sean\PycharmProjects\Kansas-Crop-Data\2020 Tables Using Union Method\\" + str(crop_types[index]) + " " + str(year))
        index += 1

def create_area_threshold_tables(thresholds_dfs, crop_types, county_distributions):
    index = 0
    for df in thresholds_dfs:
        print(df)
        df.to_csv(r"C:\Users\Sean\PycharmProjects\Kansas-Crop-Data\2020 Area Tables Using Union Method\\" + str(
            crop_types[index]) + " " + str(year))
        index += 1

    # df = pd.DataFrame(index=thresholds, columns=counties)
    # for county in counties:
    #     i = counties.index(county)
    #     df[county] = county_distributions[i]
    # filepath = Path(r"Frequency Distribution Tables\Corn Frequency Distribution Table 2016.csv")
    # filepath.parent.mkdir(parents=True, exist_ok=True)
    # df.to_csv(filepath)

# Create threshold and county table for cotton/wheat
# Remove fields with crops that are the majority and aren't being searched for before searching county csvs
# This function splits a county's dataframe into dataframes containing fields identified using the weighted algorithm approach
def weighted_county_df_splitter(threshold,county_df,split_dfs,survey_values_for_county,crop_types_for_county,crop_weights):
    # Generates the crop weights
    i = 0
    for df in split_dfs:
        area_fields = df["AREA"].sum() / 4046.86
        crop_weights[i] = survey_values_for_county[i] / area_fields
        i += 1
    weight_order = []
    # Generates the order of the crops to be checked
    for weight in crop_weights:
        min = crop_weights.min()
        index = crop_weights.index(min)
        crop_weights[index] = 0
        weight_order.append(index)
    # Splits the county_df into the crop_dfs based on the order of the weights and the current threshold
    # Single out threshold before splitting
    for index in weight_order:
        # Adds the fields with a threshold >= the current threshold in the order of the weights.
        split_dfs[index] += county_df[county_df[crop_types_for_county[index]].astype(float) >= threshold]
        # Trims the original dataframe of the fields greater than the threshold.
        county_df = county_df[crop_types_for_county[index].astype(float) < threshold]
    threshold -= 1
    if threshold >= 0:
        return weighted_county_df_splitter(threshold,county_df,split_dfs,survey_values_for_county,crop_types_for_county,crop_weights)
    return split_dfs, county_df


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
thresholds = []
for i in range(101):
    thresholds.append(i / 100)

survey_crop_dfs = []
counties_for_each_crop = []
county_names_for_each_crop = []
for crop in crop_types:
    survey_crop_df = get_counties_with_survey_data(survey_df, crop)
    counties = survey_crop_df["County"].unique().tolist()
    county_codes = get_county_code(county_information_file, counties)
    counties_for_each_crop.append(county_codes)
    county_names_for_each_crop.append(counties)
    survey_crop_dfs.append(survey_crop_df)

crop_dfs = []
for crop_id in crop_ids:
    crop_df = get_crop_threshold_df(field_df, crop_id)
    crop_dfs.append(crop_df)

county_dfs_by_crop = []
i = 0
for crop_df in crop_dfs:
    county_dfs = get_county_dfs(crop_df, counties_for_each_crop[i])
    i += 1
    county_dfs_by_crop.append(county_dfs)

print("Processing threshold crop data")
threshold_crop_data = get_threshold_crop_data(thresholds, county_dfs_by_crop, crop_ids, county_names_for_each_crop)

print("Creating threshold crop dataframes")
threshold_crop_dfs = create_threshold_dfs(threshold_crop_data, crop_ids, county_names_for_each_crop, thresholds)

create_area_threshold_tables(threshold_crop_dfs, crop_types, year)

print("Normalizing threshold values to their respective survey values")
normalized_threshold_dfs = normalize_threshold_values(survey_crop_dfs, threshold_crop_dfs)

print(normalized_threshold_dfs[-1])

print("Graphing threshold values")
graph_normalized_threshold_values(normalized_threshold_dfs, crop_types, year, thresholds)

create_threshold_tables(normalized_threshold_dfs, crop_types, year)

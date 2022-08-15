import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ONE_get_fipsstco_number
from pathlib import Path

# read input table
print("-- Read CSV database from Step 2: CLU_CDL_Cotton_2006-2020.csv")

# in_clu__str =r"C:\Users\Sean\PycharmProjects\Cotton_In_Kansas\Cotton_CLU_CDL_Kansas_2006-2020.csv"
union_file_location = r"CLU_CDL_KS_2020_UNION.txt"
majority_file_location = r"CLU_CDL_2020_MajorityCrop.txt"
# use chunks for reading large databases to save memory

i = 0
print("-- -- chunking of majority crop file begins --"),
majority_chunk_list = []
for df_chunk in pd.read_csv(
        majority_file_location,
        chunksize=10000):
    i += 1
    majority_chunk_list.append(df_chunk)

    print(" " + str(i)),

# concatenate individual chunks in a single dataframe
majority_crop_df = pd.concat(majority_chunk_list)

print(" -- chunking ends ")

# This sections adds the majority
i = 0
print("-- -- chunking of union file begins --"),
df_chunk_list = []
for df_chunk in pd.read_csv(
        union_file_location,
        chunksize=10000):
    majority_chunk = majority_chunk_list[i]
    i += 1
    crop_types = []
    # Soybeans
    df_chunk["VALUE_5"] = df_chunk["VALUE_5"] + df_chunk["VALUE_26"]
    df_chunk["VALUE_5"] = df_chunk["VALUE_5"] + df_chunk["VALUE_240"]
    df_chunk["VALUE_5"] = df_chunk["VALUE_5"] + df_chunk["VALUE_254"]

    # Corn
    df_chunk["VALUE_1"] = df_chunk["VALUE_1"] + df_chunk["VALUE_225"]
    df_chunk["VALUE_1"] = df_chunk["VALUE_1"] + df_chunk["VALUE_226"]
    df_chunk["VALUE_1"] = df_chunk["VALUE_1"] + df_chunk["VALUE_228"]

    # Cotton
    df_chunk["VALUE_2"] = df_chunk["VALUE_2"] + df_chunk["VALUE_238"]

    # Sorghum
    df_chunk["VALUE_4"] = df_chunk["VALUE_4"] + df_chunk["VALUE_236"]

    for value in df_chunk.columns.values:
        if "VALUE_" in value:
            crop_types.append(value)
    df_chunk["MAJORITY_TYPE"] = "VALUE_" + majority_chunk["MAJORITY"].astype(str)
    df_chunk["AREA"] = majority_chunk["AREA"].tolist()
    df_chunk["MAJORITY_VALUE"] = df_chunk[crop_types].max(axis=1)
    df_chunk["MAJORITY_PERCENTAGE"] = df_chunk[crop_types].max(axis=1) / df_chunk["AREA"]
    df_chunk_list.append(df_chunk)

    print(" " + str(i)),

union_df = pd.concat(df_chunk_list)
print(" -- chunking ends ")

value_locations = union_df["MAJORITY_TYPE"].tolist()
print(len(union_df))
print(len(value_locations))
# adds fipsstco column
union_df['FIPSSTCO'] = union_df['SCTFS'].astype(str).str[0:5].tolist()

# add county field to dataframe
# clu__df = clu__df.assign(col_name=
unique_ids = union_df['FIPSSTCO'].unique().tolist()
print(len(unique_ids))
county_ID, counties = ONE_get_fipsstco_number.get_county_ids_with_data()

print(county_ID)
print(len(county_ID))
print(counties)
print(len(counties))

print(union_df)

# extract for single county: Sumner = 191, State = 20 when FIPSSTCO == 20191
for county in counties:
    currentIndex = counties.index(county)
    mask = (union_df.loc[union_df['FIPSSTCO'] == str(county_ID[currentIndex])])
    mask = mask.assign(County=county)
    print(mask)
    # next line generates csvs for each county
    mask.to_csv(r"Majority Crop by County CSVs\\" + str(county) + str(county_ID[currentIndex]) + ".csv")
#
# # next lines generate a csv with all other field data
mask = (union_df.loc[~union_df['FIPSSTCO'].isin(county_ID)])
mask = mask.assign(County="OTHER (COMBINED) COUNTIES")
mask.to_csv(r"Majority Crop by County CSVs\\" + "OTHER (COMBINED) COUNTIES.csv")

# ---------------------------------------------------------------------------
# Name: 4_Cotton_CLU_County_Acres.py
# Created on: 2022-02-20 09:00:00.00000
# Created by: Aleksey Sheshukov
# Description: This script reads CLU cotton data 2006-2020 from CSV CLU database processed in Step 2 and
#       aggregates county acreage based on different majority thresholds.
#       Then it creates a table output of acreage for each county and compares with QuickStats county data.
# Input:
#   - Cotton CLU KARS database (CSV output from CLU_Cotton_CDL_AllYears.shp file (2006-2020) from Step 2
#   - Quickstats CSV county data (2006-2020)
#   -
# Output:
#   - Tables of sum of cotton acres in each county for each year
# ---------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ONE_get_fipsstco_number
from pathlib import Path

# read input table
print("-- Read CSV database from Step 2: CLU_CDL_Cotton_2006-2020.csv")

# in_clu__str =r"C:\Users\Sean\PycharmProjects\Cotton_In_Kansas\Cotton_CLU_CDL_Kansas_2006-2020.csv"
in_clu__str = r"Soybeans_CLU_CDL_Kansas_2006-2020.txt"

# use chunks for reading large databases to save memory
i = 0
print("-- -- chunking begins --"),
clu_df__lst = []
for chunk_clu__df in pd.read_csv(
        in_clu__str,
        # index_col=['OBJECTID'],
        # names=['OBJECTID', 'UID', 'SCTFS', 'Shape_Area', 'AREA_2020'],
        dtype={'UID': str, 'Acres': str, 'SCTFS': str, 'RastArea': str,
               'zm_2003': str, 'zm_2004': str, 'zm_2005': str, 'zm_2006': str, 'zm_2007': str,
               'zm_2008': str, 'zm_2009': str, 'zm_2010': str, 'zm_2011': str, 'zm_2012': str,
               'Area_acres': str, 'Shape_STAr': str, 'Shape_Length': str, 'Shape_Area': str,
               'COUNT_2006': str, 'AREA_2006': str, 'COUNT_2007': str, 'AREA_2007': str,
               'COUNT_2008': str, 'AREA_2008': str, 'COUNT_2009': str, 'AREA_2009': str,
               'COUNT_2010': str, 'AREA_2010': str, 'COUNT_2011': str, 'AREA_2011': str,
               'COUNT_2012': str, 'AREA_2012': str, 'COUNT_2013': str, 'AREA_2013': str,
               'COUNT_2014': str, 'AREA_2014': str, 'COUNT_2015': str, 'AREA_2015': str,
               'COUNT_2016': str, 'AREA_2016': str, 'COUNT_2017': str, 'AREA_2017': str,
               'COUNT_2018': str, 'AREA_2018': str, 'COUNT_2019': str, 'AREA_2019': str,
               'COUNT_2020': str, 'AREA_2020': str, 'FIPSSTCO': str, },
        # na_values=['NAN'],
        chunksize=100000):
    i += 1

    chunk_clu__df = chunk_clu__df[['UID', 'SCTFS', 'Shape_Area', 'AREA_2020', 'AREA_2019', 'AREA_2018',
                                   'AREA_2017', 'AREA_2016', 'AREA_2015', 'AREA_2014', 'AREA_2013', 'AREA_2012',
                                   'AREA_2011', 'AREA_2010', 'AREA_2009', 'AREA_2008', 'AREA_2007', 'AREA_2006']]

    clu_df__lst.append(chunk_clu__df)

    print(" " + str(i)),

# concatenate individual chunks in a single dataframe
clu__df = pd.concat(clu_df__lst)

print(" -- chunking ends ")

# adds fipsstco column
clu__df['FIPSSTCO'] = clu__df['SCTFS'].astype(str).str[0:5].tolist()
in_county__str = r"C:\Users\Sean\PycharmProjects\Kansas-Crop-Data\Cotton_County_Kansas.txt"
county__df = pd.read_csv(in_county__str)


# add county field to dataframe
# clu__df = clu__df.assign(col_name=
unique_ids = clu__df['FIPSSTCO'].unique().tolist()
print(len(unique_ids))
county_ID, counties = ONE_get_fipsstco_number.get_county_ids_with_data()


# county_ID = ['20007', '20035', '20067', '20069', '20077', '20079', '20081', '20095', '20151', '20173', '20175', '20189',
#              '20191']
# counties = ['BARBER', 'COWLEY', 'GRANT', 'GRAY', 'HARPER', 'HARVEY', 'HASKELL', 'KINGMAN',
#             'PRATT', 'SEDGEWICK', 'SEWARD', 'STEVENS', 'SUMNER']
print(county_ID)
print(len(county_ID))
print(counties)
print(len(counties))
# extract for single county: Sumner = 191, State = 20 when FIPSSTCO == 20191
for county in counties:
    currentIndex = counties.index(county)
    mask = (clu__df.loc[clu__df['FIPSSTCO'] == county_ID[currentIndex]])
    mask = mask.assign(County=county)
    # next line generates csvs for each county
    mask.to_csv(r"C:\Users\Sean\PycharmProjects\Kansas-Crop-Data\Soybeans County CSVs\\" + county + str(county_ID[currentIndex]) + ".csv")

# next lines generate a csv with all other field data
mask = (clu__df.loc[~clu__df['FIPSSTCO'].isin(county_ID)])
mask = mask.assign(County="OTHER (COMBINED) COUNTIES")
mask.to_csv(r"C:\Users\Sean\PycharmProjects\Kansas-Crop-Data\Soybeans County CSVs\\" + "OTHER (COMBINED) COUNTIES.csv")

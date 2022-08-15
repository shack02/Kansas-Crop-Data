import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def table_generator(counties, normalized_county_data, thresholds, state_normalized_data):
    df = pd.DataFrame(columns=counties, index=thresholds)
    for county in counties:
        df[county] = normalized_county_data[counties.index(county)]
    df["State"] = state_normalized_data
    filepath = Path(r'C:\Users\Sean\Desktop\2020 Graphs and Tables\Corn\Corn 2020 Table.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)


def county_distribution(counties, thresholds, county_distributions):
    df = pd.DataFrame(index=thresholds, columns=counties)
    for county in counties:
        i = counties.index(county)
        df[county] = county_distributions[i]
    filepath = Path(r"C:\Users\Sean\Desktop\2020 Graphs and Tables\Corn\Corn Frequency Distribution Table 2020.csv")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)
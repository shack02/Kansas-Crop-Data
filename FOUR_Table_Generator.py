import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def table_generator(counties, normalized_county_data, thresholds, state_normalized_data):
    df = pd.DataFrame(columns=counties, index=thresholds)
    for county in counties:
        df[county] = normalized_county_data[counties.index(county)]
    df["State"] = state_normalized_data
    filepath = Path(r'C:\Users\Sean\PycharmProjects\Cotton_In_Kansas\Tables\Corn 2016 Table.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)

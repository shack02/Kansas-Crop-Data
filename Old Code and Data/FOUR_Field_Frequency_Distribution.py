import pandas as pd
import matplotlib.pyplot as plt


def data_generator(thresholds, county_csv, year):
    county_distributions = []
    print(len(county_csv))

    for county in county_csv:
        df = pd.read_csv(county)
        df = df[df['AREA_' + year] != 0]
        df = df[df["Shape_Area"] != 0]
        df = df.assign(Percent=df["AREA_" + year] / df["Shape_Area"])
        df = df["Percent"].round(decimals=2)
        list = []
        for percent in thresholds:
            number_fields = (sum(df.iloc[:-1] == percent))
            list.append(number_fields)
        county_distributions.append(list)
    print(len(county_distributions))
    return county_distributions


def plot_counties(thresholds, county_distributions, year, counties):
    for county in county_distributions:
        i = county_distributions.index(county)
        x_axis = thresholds
        y_axis = county
        plt.bar(x_axis,y_axis, color='blue', width=.1)
        plt.xticks(x_axis[0::10])
        plt.title("Frequency Distribution for " + counties[i] + " county " + year)
        plt.ylabel('Number Fields')
        plt.xlabel('% Thresholds')
        plt.show()
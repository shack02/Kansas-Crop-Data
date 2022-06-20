import matplotlib.pyplot as plt
import pandas as pd


def extract_survey_data():
    csv = "Other Crop Data (Corn and Sorghum).csv"
    df = pd.read_csv(csv)
    print(df)
    df = df[df["Data Item"] == "CORN - ACRES PLANTED"]
    print(df)

    counties = df["County"].unique().tolist()
    counties.sort()
    print('***HERE***')
    print(counties)

    values_for_each_county = []
    years_for_each_county = []
    for county in counties:
        subset_df = df[df["County"] == county]
        years = subset_df["Year"].tolist()
        years_for_each_county.append(years)
        values = subset_df["Value"].tolist()
        values = [i.replace(',', '') for i in values]
        values = [int(i) for i in values]
        values_for_each_county.append(values)

    survey_year_values = []
    i = 0
    while i < len(years_for_each_county):
        j = 0
        while j < len(years_for_each_county[i]):
            if years_for_each_county[i][j] == 2017:
                survey_year_values.append(values_for_each_county[i][j])
            j += 1
        i += 1
    print(survey_year_values)

    return years_for_each_county, values_for_each_county, counties


def plot_survey_graphs(years_for_each_county, values_for_each_county, counties):
    for county in counties:
        current_index = counties.index(county)
        x_axis = years_for_each_county[current_index]
        y_axis = values_for_each_county[current_index]
        plt.bar(x_axis, y_axis)
        plt.xticks(x_axis)
        plt.title(county + " Survey: Corn Acres Planted")
        plt.xlabel("Year")
        plt.ylabel("Value")
        # plot = plt.figure(counties.index(county))
        plt.show()

#
# def generate_survey_table(years_for_each_county, values_for_each_county, counties):
#     years = [2021, 2020, 2019, 2018, 2017, 2016]
#     for county in counties:
#         for year in years:
#          # if year not in years_for_each_county[counties.index(county)]

    # df = pd.DataFrame(columns=counties, index=thresholds)
    # for county in counties:
    #     df[county] = normalized_county_data[counties.index(county)]
    # df["State"] = state_normalized_data
    # filepath = Path(r'C:\Users\Sean\PycharmProjects\Cotton_In_Kansas\Tables\Corn 2016 Table.csv')
    # filepath.parent.mkdir(parents=True, exist_ok=True)
    # df.to_csv(filepath)

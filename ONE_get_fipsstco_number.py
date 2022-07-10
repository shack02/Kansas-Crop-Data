import pandas as pd
import ONE_Corn_Survey_Data


def get_county_ids_with_data():
    in_county__str = r"Cotton_County_Kansas.txt"
    county__df = pd.read_csv(in_county__str)

    county_ID = county__df["FIPSSTCO"].tolist()
    counties = county__df["COUNTY"].tolist()

    counties = sorted(counties)
    county_ID = sorted(county_ID)

    years_for_each_county, values_for_each_county, counties_with_data = ONE_Corn_Survey_Data.extract_survey_data()

    counties = [county.upper() for county in counties]

    return county_ID, counties

    # county_id_with_data = []
    # proper_counties = []
    # for county in counties:
    #     i = counties.index(county)
    #     for county2 in counties_with_data:
    #         if county2 == county:
    #             county_id_with_data.append(str(county_ID[i]))
    #             proper_counties.append(county)
    #
    # return county_id_with_data, proper_counties


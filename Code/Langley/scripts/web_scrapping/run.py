import time

from bot import Bot
import pandas as pd

df = pd.read_csv('Address_Points.csv')

# Extract all unique FOLIO values

gross_data_list = []
land_data_list = []
improvement_data_list = []
gross_df = pd.DataFrame(columns=["FOLIO", "ADDRESS", "2024", "2023", "2022", "2021", "2020"])
land_df = pd.DataFrame(columns=["FOLIO", "ADDRESS", "2024", "2023", "2022", "2021", "2020"])
improvement_df = pd.DataFrame(columns=["FOLIO", "ADDRESS", "2024", "2023", "2022", "2021", "2020"])

with Booking() as bot:
    for index, row in df.iloc[0:].iterrows():
        bot.land_first_page()

        folio = row['FOLIO']
        address = row['FULL_ADD']
        print(folio)

        bot.input_folio(folio)
        bot.search()

        response = bot.go_to_result()
        if response == 0:
            land_values, improvement_values, gross_assessment, response = bot.get_table()
        else:
            land_values = ['0'] * 5
            improvement_values = ['0'] * 5
            gross_assessment = ['0'] * 5

        gross_assessment.insert(0, folio)
        gross_assessment.insert(1, address)
        land_values.insert(0, folio)
        land_values.insert(1, address)
        improvement_values.insert(0, folio)
        improvement_values.insert(1, address)


        gross_df.loc[len(gross_df.index)] = gross_assessment
        land_df.loc[len(land_df.index)] = land_values
        improvement_df.loc[len(improvement_df.index)] = improvement_values


        if index % 100 == 0:
            if index == 0:
                gross_df.to_csv('gross_assessment_2020_2024.csv', index=False)
                land_df.to_csv('land_assessment_2020_2024.csv', index=False)
                improvement_df.to_csv('improvement_assessment_2020_2024.csv', index=False)
            else:
                gross_df.to_csv('gross_assessment_2020_2024.csv', mode='a', header=False, index=False)
                land_df.to_csv('land_assessment_2020_2024.csv', mode='a', header=False, index=False)
                improvement_df.to_csv('improvement_assessment_2020_2024.csv', mode='a', header=False, index=False)

            gross_df.drop(gross_df.index, inplace=True)
#             land_df.drop(land_df.index, inplace=True)
#             improvement_df.drop(improvement_df.index, inplace=True)

    gross_df.to_csv('gross_assessment_2020_2024.csv', mode='a', header=False, index=False)
#     land_df.to_csv('land_assessment_2020_2024.csv', mode='a', header=False, index=False)
#     improvement_df.to_csv('improvement_assessment_2020_2024.csv', mode='a', header=False, index=False)

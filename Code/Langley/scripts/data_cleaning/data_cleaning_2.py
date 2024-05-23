# Find the POSTAL CODE for each STREET, Find the Count_Per_Year for each POSTAL CODE and find the coordinates for each postal code.
import pandas as pd

postal = pd.read_csv('street_postal_cleaned.csv')
street_averages = pd.read_csv('land_improvement.csv')
coord = pd.read_csv('CanadianPostalCodes202312.csv')
columns = ['CURRENT_LAND_VALUE_2024',
                                     'CURRENT_LAND_VALUE_2023','CURRENT_LAND_VALUE_2022',
                                     'CURRENT_LAND_VALUE_2021','CURRENT_LAND_VALUE_2020',
                                     'CURRENT_IMPROVEMENT_VALUE_2024','CURRENT_IMPROVEMENT_VALUE_2023',
                                     'CURRENT_IMPROVEMENT_VALUE_2022','CURRENT_IMPROVEMENT_VALUE_2021',
                                     'CURRENT_IMPROVEMENT_VALUE_2020','LATITUDE','LONGITUDE']
merged_df = pd.merge(street_averages, postal, on='STREET')
for i in range(5):
    col = f'Count_Per_Year_{2020+i}'
    merged_df[col] = merged_df.groupby('POSTAL CODE')['POSTAL CODE'].transform('count')
    columns.append(col)
merged_df = merged_df.groupby('POSTAL CODE').sum().reset_index()
merged_df = merged_df.rename(columns={'POSTAL CODE': 'POSTAL_CODE'})
merged_df = pd.merge(merged_df, coord, on='POSTAL_CODE')

merged_df = merged_df[columns]
merged_df.to_csv('postal_code_land_values.csv', index=False)



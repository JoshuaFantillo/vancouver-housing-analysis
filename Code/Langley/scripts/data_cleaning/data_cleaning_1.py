##Combine the land values with improvement values and rename the columns
import pandas as pd

df = pd.read_csv('land_values_cleaned.csv')
improvement = pd.read_csv('improvement_assessment_2020_2024.csv')

df['STREET'] = df['ADDRESS'].apply(lambda x: ' '.join(x.split()[-2:]))

land_improvement = pd.merge(df, improvement, on='FOLIO')
land_improvement = land_improvement[['STREET','CURRENT_LAND_VALUE_2024',
                                     'CURRENT_LAND_VALUE_2023','CURRENT_LAND_VALUE_2022',
                                     'CURRENT_LAND_VALUE_2021','CURRENT_LAND_VALUE_2020',
                                     '2024','2023','2022','2021','2020']]
land_improvement = land_improvement.rename(columns={'2024': 'CURRENT_IMPROVEMENT_VALUE_2024', '2023': 'CURRENT_IMPROVEMENT_VALUE_2023', '2022': 'CURRENT_IMPROVEMENT_VALUE_2022', '2021': 'CURRENT_IMPROVEMENT_VALUE_2021', '2020': 'CURRENT_IMPROVEMENT_VALUE_2020'})


land_improvement.to_csv('land_improvement.csv', index=False)


import pandas as pd

lat_long = pd.read_csv('scripts/data/area_lat_long.csv')

def get_coordinates(region):
    record = lat_long[lat_long['Region'] == region]
    if not record.empty:
        return float(record['Lat'].values[0]), float(record['Long'].values[0])
    return None, None
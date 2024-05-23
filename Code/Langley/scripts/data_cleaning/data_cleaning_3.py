#Find the values for MIN_DISTANCE_LIBRARY_METERS, CLOSEST_SCHOOL_METERS etc.
import pandas as pd

from math import radians, sin, cos, sqrt, atan2

library = pd.read_csv('libraries.csv')
school = pd.read_csv('schools.csv')
shelters = pd.read_csv('shelters.csv')
comm = pd.read_csv('community-center.csv')
dog = pd.read_csv('dog-park.csv')
df = pd.read_csv('postal_code_land_values.csv')

def haversine(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    radius_earth = 6371000  # Radius of Earth in meters
    distance = radius_earth * c

    return distance

def min_library(lat, long):
    min = 999999
    for index, row in library.iterrows():
        lib_lat, lib_long = row['LAT'], row['LONG']
        distance = haversine(lat,long,lib_lat,lib_long)
        if distance < min:
            min = distance
    return min

def min_shelter(lat, long):
    min = 999999
    for index, row in shelters.iterrows():
        shel_lat, shel_long = row['LAT'], row['LONG']
        distance = haversine(lat,long,shel_lat,shel_long)
        if distance < min:
            min = distance
    return min

def min_school(lat, long):
    min = 999999
    for index, row in shelters.iterrows():
        school_lat, school_long = row['LAT'], row['LONG']
        distance = haversine(lat,long,school_lat,school_long)
        if distance < min:
            min = distance
    return min

def min_comm(lat, long):
    min = 999999
    for index, row in comm.iterrows():
        comm_lat, comm_long = row['LAT'], row['LONG']
        distance = haversine(lat,long,comm_lat, comm_long)
        if distance < min:
            min = distance
    return min

def min_dog(lat, long):
    min = 999999
    for index, row in dog.iterrows():
        dog_lat, dog_long = row['LAT'], row['LONG']
        distance = haversine(lat,long,dog_lat, dog_long)
        if distance < min:
            min = distance
    return min

for index, row in df.iterrows():
    lat, long = row['LATITUDE'], row['LONGITUDE']
    df.at[index, 'MIN_DISTANCE_LIBRARY_METERS'] = min_library(lat, long)
    df.at[index, 'CLOSEST_HOMELESS_SHELTER'] = min_shelter(lat, long)
    df.at[index, 'CLOSEST_SCHOOL_METERS'] = '{'+str(min_school(lat,long)) + ", Public School}"
    df.at[index, 'COMMUNITY_CENTRE_DISTANCE_METERS'] = min_comm(lat, long)
    df.at[index, 'CLOSEST_DOG_PARK_METERS'] = min_comm(lat, long)
    df.at[index, 'YEAR_BUILT'] = 1700
    df.at[index, 'BIG_IMPROVEMENT_YEAR'] = 1700


df.to_csv('cleaned.csv', index=False)
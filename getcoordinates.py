
from geopy.geocoders import ArcGIS
from geopy.exc import GeocoderTimedOut


geolocator = ArcGIS(user_agent="geoapiExercises")
# Define a function to get coordinates from postal code
def get_coordinates(postal_code):
    if postal_code is not None:
        try:
            location = geolocator.geocode(postal_code)
            if location is not None:
                return (location.latitude, location.longitude)
        except GeocoderTimedOut:
            return get_coordinates(postal_code)
    return None, None


#An example of applying the function to the 'postal_code' column and create a new 'coordinates' column
df['coordinates'] = df['postal_code'].apply(get_coordinates)



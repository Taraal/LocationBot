import json

# Retrieve all data in loc.json file
def get_file_data():
    with open('loc.json', 'r') as f:
        data = json.load(f)
    return data

# Write new line in loc.json file
def write_file_data(data):
    with open('loc.json', 'w') as f:
        json.dump(data, f)


# Retrieve Gmaps url depending of datas stored in loc.json file.
"""
For the user who's calling bot, if he has only one data stored we will return a single coordinate point.
If the user has two point we will set up an origin point and a destination point by tracing the travel line between these two points.
If the user has more than two points set, the points between first and last point are defined as waypoints.
"""
def get_map_url(locations):
    SEARCH_URL = "https://www.google.com/maps/search/?api=1&query="
    DIRECTIONS_URL = " https://www.google.com/maps/dir/?api=1&"
    if len(locations) == 1:
        return f"{SEARCH_URL}{locations[0]['coordinates']}"

    if len(locations) == 2:
        return f"{DIRECTIONS_URL}origin={locations[0]['coordinates']}&destination={locations[1]['coordinates']}"

    if len(locations) > 2:
        origin = locations[0]['coordinates']
        destination = locations[-1]['coordinates']
        waypoints = []
        for location in locations[1:-1]:
            waypoints.append(location['coordinates'])
        waypoints_url = "|".join(waypoints)
        print(waypoints)
        return f"{DIRECTIONS_URL}origin={origin}&destination={destination}&waypoints={waypoints_url}"

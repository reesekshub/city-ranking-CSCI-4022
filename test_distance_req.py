from distance_requests import get_distances


results = get_distances("Boulder, CO", "bicycling")
print(results[("home", "downtown")])
# {'distance_m': 3200, 'distance_text': '3.2 km', 'duration_s': 720, 'duration_text': '12 mins'}
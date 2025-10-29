# cuopt.py
def get_routes(start, end):
    """
    Mock NVIDIA cuOpt optimizer: returns sample route options.
    In a real app, this would call the cuOpt API or SDK.
    """

    routes = [
        {
            "route": f"{start} → {end} via Downtown",
            "distance": 6.0,   # km
            "time": 12,        # minutes
            "co2": 0.72,       # kg CO2
            "aqi": 70          # air quality index
        },
        {
            "route": f"{start} → {end} via Parkside",
            "distance": 6.8,
            "time": 14,
            "co2": 0.82,
            "aqi": 40
        }
    ]

    return routes

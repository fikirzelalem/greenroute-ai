def calculate_emissions(start, end):
    # Mock data for demo
    routes = [
        {"route": f"{start} → {end} via Downtown", "distance": 6.0, "time": 12, "aqi": 70},
        {"route": f"{start} → {end} via Parkside", "distance": 6.8, "time": 14, "aqi": 40},
    ]

    # Estimate CO₂ (0.12 kg/km)
    for r in routes:
        r["co2"] = r["distance"] * 0.12
    return routes

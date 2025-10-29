def call_nemotron(routes):
    greener = min(routes, key=lambda x: x["co2"] + x["aqi"] * 0.01)
    alt = [r for r in routes if r != greener][0]

    return (
        f"After analyzing emissions and air quality data, the AI agent "
        f"recommends **{greener['route']}** as the greenest route.\n\n"
        f"It produces **{alt['co2'] - greener['co2']:.2f} kg less CO₂** "
        f"and avoids high-pollution zones (AQI improvement of {alt['aqi'] - greener['aqi']} points). "
        f"This choice helps reduce fuel use and improve neighborhood air quality."
    )

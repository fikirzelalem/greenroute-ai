import streamlit as st
from llm_agent import call_nemotron
from emissions import calculate_emissions
import folium
from streamlit_folium import st_folium

# Create a small mock map
m = folium.Map(location=[38.918, -77.02], zoom_start=13, tiles="CartoDB dark_matter")

# Add two simple routes
folium.PolyLine([(38.918, -77.02), (38.91, -77.045)], color="gray", weight=4, opacity=0.6).add_to(m)
folium.PolyLine([(38.918, -77.02), (38.92, -77.03)], color="green", weight=5, opacity=0.8).add_to(m)

st.write("### 🗺️ Route Visualization")
st_folium(m, width=700, height=400)

st.set_page_config(page_title="GreenRoute AI", page_icon="🌿", layout="centered")

st.title("GreenRoute AI 🚗🌿")
st.subheader("Built for the NVIDIA Agents for Impact Hackathon @ Howard University")

st.write("Enter your start and destination points to find the **greenest** route available.")

start = st.text_input("Start Location", placeholder="e.g., Howard University")
end = st.text_input("Destination", placeholder="e.g., Georgetown University")

if st.button("Find Green Route"):
    with st.spinner("Analyzing routes..."):
        routes = calculate_emissions(start, end)
        explanation = call_nemotron(routes)

    st.success("✅ Analysis Complete")

    st.write("### 🌍 Route Comparison")
    for r in routes:
        st.write(
            f"**{r['route']}** — Distance: {r['distance']} km | "
            f"Time: {r['time']} min | CO₂: {r['co2']:.2f} kg | AQI: {r['aqi']}"
        )

    st.divider()
    st.write("### 🤖 NVIDIA Agent Reasoning")
    st.write(explanation)

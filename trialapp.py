import streamlit as st

# Set page configuration
st.set_page_config(page_title="AQI App", page_icon="🌫️", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            font-size:50px;
            font-weight:bold;
            color:#2E86C1;
            text-align:center;
            margin-bottom:30px;
        }
        .info {
            background-color: #D6EAF8;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0px;
        }
    </style>
""", unsafe_allow_html=True)

# Title with custom style
st.markdown('<div class="title">WELCOME TO THE AQI APP!</div>', unsafe_allow_html=True)

# Sample AQI input
st.markdown('<div class="info">Enter your city below to get the Air Quality Index:</div>', unsafe_allow_html=True)
station = st.text_input("City Name")

if station:
    import pandas as pd

# === AQI Calculation Functions ===
def calculate_aqi(concentration, breakpoints):
    for Clow, Chigh, Ilow, Ihigh in breakpoints:
        if Clow <= concentration <= Chigh:
            return round((Ihigh - Ilow) / (Chigh - Clow) * (concentration - Clow) + Ilow)
    return 0  # Return 0 instead of None

def classify_aqi(aqi):
    if pd.isna(aqi) or aqi < 0 or aqi > 500:
        return ("Invalid", "Gray", "Invalid AQI value")
    elif aqi <= 50:
        return ("Good", "Green", "Air quality is satisfactory.")
    elif aqi <= 100:
        return ("Moderate", "Yellow", "Acceptable; some pollutants may affect sensitive individuals.")
    elif aqi <= 150:
        return ("Unhealthy for Sensitive Groups", "Orange", "Sensitive people may experience health effects.")
    elif aqi <= 200:
        return ("Unhealthy", "Red", "Everyone may begin to experience health effects.")
    elif aqi <= 300:
        return ("Very Unhealthy", "Purple", "Health alert: serious effects for everyone.")
    else:
        return ("Hazardous", "Maroon", "Emergency conditions: serious risk to health for everyone.")

def aqi_for_all_pollutants(values):
    breakpoints_data = {
        'PM2.5': [(0.0, 12.0, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150), (55.5, 150.4, 151, 200), (150.5, 250.4, 201, 300), (250.5, 350.4, 301, 400), (350.5, 500.4, 401, 500)],
        'PM10':  [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150), (255, 354, 151, 200), (355, 424, 201, 300), (425, 504, 301, 400), (505, 604, 401, 500)],
        'NO2':   [(0, 53, 0, 50), (54, 100, 51, 100), (101, 360, 101, 150), (361, 649, 151, 200), (650, 1249, 201, 300), (1250, 1649, 301, 400), (1650, 2049, 401, 500)],
        'SO2':   [(0, 35, 0, 50), (36, 75, 51, 100), (76, 185, 101, 150), (186, 304, 151, 200), (305, 604, 201, 300), (605, 804, 301, 400), (805, 1004, 401, 500)],
        'CO':    [(0.0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150), (12.5, 15.4, 151, 200), (15.5, 30.4, 201, 300), (30.5, 40.4, 301, 400), (40.5, 50.4, 401, 500)],
        'O3':    [(0, 54, 0, 50), (55, 70, 51, 100), (71, 85, 101, 150), (86, 105, 151, 200), (106, 200, 201, 300), (201, 300, 301, 400), (301, 400, 401, 500)]
    }

    individual_aqi = {}
    for pollutant, value in values.items():
        bp = breakpoints_data.get(pollutant)
        if bp and pd.notnull(value):
            individual_aqi[pollutant] = calculate_aqi(value, bp)

    if individual_aqi and all(val is None for val in individual_aqi.values()):
        overall_aqi = None
    else:
        overall_aqi = max(val for val in individual_aqi.values() if val is not None) if individual_aqi else None

    return overall_aqi, individual_aqi

# === Load your CSV ===
df = pd.read_csv("combined_output.csv")

# === Calculate AQI and Bucket row by row ===
aqi_values = []
aqi_buckets = []
aqi_colors = []
aqi_messages = []

for _, row in df.iterrows():
    pollutant_values = {
        'PM2.5': row.get('PM2.5'),
        'PM10': row.get('PM10'),
        'NO2': row.get('NO2'),
        'SO2': row.get('SO2'),
        'CO': row.get('CO'),
        'O3': row.get('O3')
    }
    overall_aqi, _ = aqi_for_all_pollutants(pollutant_values)
    bucket, color, message = classify_aqi(overall_aqi)

    aqi_values.append(overall_aqi)
    aqi_buckets.append(bucket)
    aqi_colors.append(color)
    aqi_messages.append(message)

# === Add results to DataFrame and save ===
df['AQI'] = aqi_values
df['AQI_Bucket'] = aqi_buckets
df['AQI_Color'] = aqi_colors
df['AQI_Message'] = aqi_messages
    # Dummy AQI output for example
    aqi = 85  # you would fetch this from an API or dataset
    st.success(f"The current AQI for **{city}** is: **{aqi}**")

    # Provide air quality level color coding
    if aqi <= 50:
        st.markdown("🟢 **Good**")
    elif aqi <= 100:
        st.markdown("🟡 **Moderate**")
    elif aqi <= 150:
        st.markdown("🟠 **Unhealthy for Sensitive Groups**")
    elif aqi <= 200:
        st.markdown("🔴 **Unhealthy**")
    elif aqi <= 300:
        st.markdown("🟣 **Very Unhealthy**")
    else:
        st.markdown("⚫ **Hazardous**")

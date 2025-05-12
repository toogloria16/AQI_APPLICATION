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
city = st.text_input("City Name")

if city:
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

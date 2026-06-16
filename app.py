import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="IndiGo Route Intelligence",
    page_icon="✈️",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():

    profitability = pd.read_csv(
        "data/processed/indigo_profitability.csv"
    )

    network = pd.read_csv(
        "data/processed/indigo_network_intelligence.csv"
    )

    forecast = pd.read_csv(
        "data/processed/indigo_forecast.csv"
    )

    simulation = pd.read_csv(
        "data/processed/indigo_simulation_results.csv"
    )

    return profitability, network, forecast, simulation


profitability, network, forecast, simulation = load_data()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.title("✈️ IndiGo Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Dashboard",
        "Route Profitability",
        "Network Intelligence",
        "Forecasting",
        "Strategy Simulator"
    ]
)

# -------------------------------------------------
# EXECUTIVE DASHBOARD
# -------------------------------------------------

if page == "Executive Dashboard":

    st.title(
        "IndiGo Route Profitability & Network Expansion Intelligence"
    )

    revenue = profitability["Revenue"].sum()

    profit = profitability["Profit"].sum()

    margin = (
        profit / revenue
    ) * 100

    total_routes = len(profitability)

    airports = pd.concat(
        [
            profitability["Source_Airport_Name"],
            profitability["Destination_Airport_Name"]
        ]
    ).nunique()

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Revenue",
        f"₹{revenue/1e9:.2f}B"
    )

    c2.metric(
        "Profit",
        f"₹{profit/1e9:.2f}B"
    )

    c3.metric(
        "Margin",
        f"{margin:.2f}%"
    )

    c4.metric(
        "Routes",
        total_routes
    )

    c5.metric(
        "Airports",
        airports
    )

    st.divider()

    top_routes = profitability.nlargest(
        10,
        "Profit"
    )

    fig = px.bar(
        top_routes,
        x="Profit",
        y="Route",
        orientation="h",
        title="Top 10 Profitable Routes"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------
# ROUTE PROFITABILITY
# -------------------------------------------------

elif page == "Route Profitability":

    st.title("Route Profitability Explorer")

    route = st.selectbox(
        "Select Route",
        profitability["Route"].unique()
    )

    route_df = profitability[
        profitability["Route"] == route
    ]

    st.dataframe(route_df)

    st.metric(
        "Revenue",
        f"₹{route_df['Revenue'].iloc[0]/1e6:.2f}M"
    )

    st.metric(
        "Profit",
        f"₹{route_df['Profit'].iloc[0]/1e6:.2f}M"
    )

    st.metric(
        "Margin",
        f"{route_df['Profit_Margin'].iloc[0]:.2f}%"
    )

# -------------------------------------------------
# NETWORK INTELLIGENCE
# -------------------------------------------------

elif page == "Network Intelligence":

    st.title("Network Intelligence")

    st.subheader(
        "Top Hub Airports"
    )

    hubs = network.sort_values(
        "Connectivity_Score",
        ascending=False
    ).head(15)

    fig = px.bar(
        hubs,
        x="Connectivity_Score",
        y="Airport",
        orientation="h",
        title="Top Hub Airports"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Network Intelligence Dataset"
    )

    st.dataframe(network)

# -------------------------------------------------
# FORECASTING
# -------------------------------------------------

elif page == "Forecasting":

    st.title(
        "Passenger Demand Forecast"
    )

    forecast["Month"] = pd.to_datetime(
        forecast["Month"]
    )

    fig = px.line(
        forecast,
        x="Month",
        y="Forecast_Passengers",
        title="Passenger Forecast"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig2 = px.line(
        forecast,
        x="Month",
        y="Forecast_Revenue",
        title="Revenue Forecast"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -------------------------------------------------
# STRATEGY SIMULATOR
# -------------------------------------------------

elif page == "Strategy Simulator":

    st.title(
        "IndiGo Strategy Simulator"
    )

    fuel_change = st.slider(
        "Fuel Cost Change %",
        -20,
        50,
        0
    )

    ticket_change = st.slider(
        "Ticket Price Change %",
        -20,
        30,
        0
    )

    load_change = st.slider(
        "Load Factor Change %",
        -10,
        20,
        0
    )

    revenue = profitability["Revenue"].sum()

    profit = profitability["Profit"].sum()

    simulated_revenue = revenue * (
        1 + ticket_change/100
    )

    simulated_profit = profit * (
        1
        + ticket_change/100
        + load_change/100
        - fuel_change/100
    )

    st.metric(
        "Projected Revenue",
        f"₹{simulated_revenue/1e9:.2f}B"
    )

    st.metric(
        "Projected Profit",
        f"₹{simulated_profit/1e9:.2f}B"
    )

    st.subheader(
        "Scenario Results"
    )

    st.dataframe(simulation)

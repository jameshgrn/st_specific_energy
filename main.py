# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define constants
g = 9.81

# Web app title and introduction
st.title("Specific Head Diagram and Open-Channel Flow")
st.write("""
The specific head (Ho) is the energy head relative to the channel bottom, which is the sum of the velocity head (
U^2/2g) and the depth (d). The specific head diagram shows the relationship between the specific head and the depth 
for a given discharge per unit width (q) in an open-channel flow. The specific head diagram has two branches: an 
upper branch for subcritical flow (Froude number less than one) and a lower branch for supercritical flow (Froude 
number greater than one). The point of vertical tangent between the two branches corresponds to the critical flow (
Froude number equal to one).

The following equations are used to calculate the specific head and the Froude number for a given flow:

Ho = d + U^2/2g

q^2 = g d^3

Fr = U / (g d)^1/2

The following equation is used to calculate the specific head downstream of a step up or down in the channel bottom:

Ho2 = Ho1 - (ho2 - ho1)

where ho is the channel bottom elevation.

This web app allows you to visualize the specific head diagram and the flows stepping up or down in an open-channel 
flow.
""")

# Input parameters
st.sidebar.header("Input parameters")

q = st.sidebar.slider("Discharge per unit width (q)", 0.0, 10.0, 5.0)
ho = st.sidebar.number_input("Channel bottom elevation (ho)", 0.0, 10.0, 5.0)
delta_h = st.sidebar.slider("Change in channel bottom elevation (delta h)", -10.0, 10.0, 0.0)

# Calculate specific head and depth
d = np.linspace(0.01, 10, 100)
Ho = q ** 2 / (2 * g * d ** 2) + d
df = pd.DataFrame({"Depth": d, "Specific Head": Ho})

# Calculate approaching and downstream flow properties
d1 = ho + q ** 2 / (2 * g * ho ** 2)
Ho1 = ho + d1
Ho2 = Ho1 - delta_h
d2 = np.interp(Ho2, df["Specific Head"], df["Depth"])

# Calculate velocities and Froude numbers
U1 = q / d1
U2 = q / d2
Fr1 = U1 / np.sqrt(g * d1)
Fr2 = U2 / np.sqrt(g * d2)


# Plot channel figure
def plot_channel(ho1, delta_h, d1, d2):
    fig, ax = plt.subplots()

    x = [0, 1, 2, 3]
    y = [ho1, ho1, ho1 + delta_h, ho1 + delta_h]

    ax.plot(x, y, color = 'black', linewidth = 2)

    # Approaching flow
    ax.fill_between([0, 1], ho1, ho1 + d1, color = 'blue', alpha = 0.5)

    # Downstream flow
    ax.fill_between([2, 3], ho1 + delta_h, ho1 + delta_h + d2, color = 'blue', alpha = 0.5)

    ax.set_ylim(0, ho1 + max(d1, d2) + 2)
    ax.set_xlim(0, 3)
    ax.set_xlabel("Horizontal distance")
    ax.set_ylabel("Elevation")
    ax.set_title("Channel Figure")

    return fig


channel_fig = plot_channel(ho, delta_h, d1, d2)
st.pyplot(channel_fig)


# Plot specific energy diagram
def plot_specific_energy(df, d1, d2):
    fig, ax = plt.subplots()

    ax.plot(df["Depth"], df["Specific Head"], label = "q = {:.2f}".format(q))
    ax.scatter(d1, Ho1, color = "red", label = "P1")
    ax.scatter(d2, Ho2, color = "green", label = "P2")
    ax.annotate("P1", (d1, Ho1))
    ax.annotate("P2", (d2, Ho2))

    ax.set_xlabel("Depth (d)")
    ax.set_ylabel("Specific Head (Ho)")
    ax.set_title("Specific Head Diagram")
    ax.legend()

    return fig


specific_energy_fig = plot_specific_energy(df, d1, d2)
st.pyplot(specific_energy_fig)

# Display flow parameters
st.markdown("## Flow parameters")
st.markdown(f"Depth of approaching flow: {d1:.2f}")
st.markdown(f"Velocity of approaching flow: {U1:.2f}")
st.markdown(f"Froude number of approaching flow: {Fr1:.2f}")
st.markdown(f"Depth of downstream flow: {d2:.2f}")
st.markdown(f"Velocity of downstream flow: {U2:.2f}")
st.markdown(f"Froude number of downstream flow: {Fr2:.2f}")


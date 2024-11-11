import streamlit as st
import matplotlib.pyplot as plt
import utils
import maximum_flow

# Title and description
st.title("Interactive Plotting App")
st.write("Select a district to visualize its road network and calculate maximum flow between streets.")

# User input for district selection
option = st.selectbox(
    "What district do you want to show?",
    ("District 10", "District Binh Thanh", "District Tan Binh"),
)

# Check if 'graph', 'street_names', and 'fig' are in session state; if not, initialize them
if "graph" not in st.session_state:
    st.session_state.graph = None
if "street_names" not in st.session_state:
    st.session_state.street_names = []
if "fig" not in st.session_state:
    st.session_state.fig = None

# Generate Network Plot button logic
if st.button("Generate Network Plot"):
    st.write(f"Showing road network for: {option}")
    graph, street_names, fig, ax = utils.plot_map(option)
    
    # Store in session state
    st.session_state.graph = graph
    st.session_state.street_names = street_names
    st.session_state.fig = fig

# Display the initial network plot if it exists in session state
if st.session_state.fig is not None:
    st.write("### Network Plot")
    st.pyplot(st.session_state.fig)

# Display the street options only if the graph and street names are loaded
if st.session_state.graph is not None:
    st.write("### Select Streets for Maximum Flow Calculation")
    
    # Allow user to select starting and destination streets
    street1 = st.selectbox("Choose starting street (node1):", st.session_state.street_names, key="street1")
    street2 = st.selectbox("Choose destination street (node2):", st.session_state.street_names, key="street2")
    
    # Only show the "Generate Maximum Flow" button if both streets have been selected
    if street1 and street2:
        if st.button("Generate Maximum Flow"):
            max_flow_value, fig2, ax2 = utils.find_maximum_flow(st.session_state.graph, street1, street2)
            
            if max_flow_value is not None:
                st.write(f"The maximum flow from {street1} to {street2} using Dinitz's algorithm is: {max_flow_value}")
                
                # Display the maximum flow plot in a separate container
                st.write("### Maximum Flow Plot")
                st.pyplot(fig2)
            else:
                st.write("Error: Unable to calculate maximum flow. Please check your input and try again.")

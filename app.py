import osmnx as ox
import networkx as nx
from pyvis.network import Network
import streamlit as st

# Define area of interest
place_name = "District 10, Ho Chi Minh City, Vietnam"
graph = ox.graph_from_place(place_name, network_type="drive")

# Convert the NetworkX graph to a Pyvis network
net = Network(notebook=True)

# Add nodes and edges to the Pyvis network
for node in graph.nodes(data=True):
    net.add_node(node[0], title=node[1]['name'] if 'name' in node[1]
                 else '', x=node[1]['x'], y=node[1]['y'])

for u, v, data in graph.edges(data=True):
    net.add_edge(u, v)

# Set up the Streamlit app
st.title("Road Network Visualization")
st.write(f"Visualizing the road network for {place_name}")

# Render the network in the Streamlit app
net.show('network.html')

# Display the HTML file in the Streamlit app
HtmlFile = open('network.html', 'r', encoding='utf-8')
source_code = HtmlFile.read()
st.components.v1.html(source_code, height=800, scrolling=True)

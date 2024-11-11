# map_utils.py
import osmnx as ox
import matplotlib.pyplot as plt
import random 
import networkx as nx
import maximum_flow
def plot_map(district):
    place_name = f"{district}, Ho Chi Minh City, Vietnam"

    graph = ox.graph_from_place(place_name, network_type="drive")
    street_names = set()
    for u, v, k, data in graph.edges(keys=True, data=True):
        if 'name' in data:
            # Add the street name(s) to the set
            if isinstance(data['name'], list):
                street_names.update(data['name'])
            else:
                street_names.add(data['name'])
    # Set up the figure with a white background
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
    ax.set_facecolor('white')  # Set axis background to white as well
    
    # Plot the graph with black edges
    ox.plot_graph(graph, ax=ax, node_size=0, edge_color='black', show=False, close=False)
    
    return graph, street_names, fig, ax

def find_nearest_node(graph, street_name):
    for u, v, data in graph.edges(data=True):
        if 'name' in data and data['name'] == street_name:
            return u  # Return the starting node of the edge
    return None

def find_maximum_flow(graph, street1, street2):
    node1 = find_nearest_node(graph, street1)
    node2 = find_nearest_node(graph, street2)

    if node1 is None or node2 is None:
        print("One of the streets was not found.")
    else:
        # Create a directed graph with random capacities
        flow_graph = nx.DiGraph()
        for u, v, data in graph.edges(data=True):
            capacity = random.randint(1, 18888)  # Assign random capacity
            flow_graph.add_edge(u, v, capacity=capacity)
            flow_graph.add_edge(v, u, capacity=capacity)

        # Calculate max flow using custom Dinitz's algorithm
        dinitz_algo = maximum_flow.DinitzMaxFlow(flow_graph, node1, node2)
        max_flow_value = dinitz_algo.max_flow()
        print(f"The maximum flow from {street1} to {street2} using Dinitz's algorithm is: {max_flow_value}")
        fig, ax = plt.subplots(figsize=(10, 10))  # You can adjust the size as needed
        ax.set_facecolor('white')  # Set the background color to white
        ox.plot_graph(graph, node_size=0, edge_color='gray', ax=ax, show=False)

        # Get the flow path for visualization
        flow_path = nx.shortest_path(flow_graph, source=node1, target=node2)

        # Extract edges of the flow path for plotting
        flow_edges = list(zip(flow_path[:-1], flow_path[1:]))

        # Plot flow path in red
        for u, v in flow_edges:
            ax.add_line(plt.Line2D([graph.nodes[u]['x'], graph.nodes[v]['x']],
                                    [graph.nodes[u]['y'], graph.nodes[v]['y']],
                                    color='red', linewidth=2))

        # Add street name annotations
        pos_street1 = graph.nodes[node1]
        pos_street2 = graph.nodes[node2]
        
        ax.text(pos_street1['x'], pos_street1['y'], street1, fontsize=12, ha='right', color='black')
        ax.text(pos_street2['x'], pos_street2['y'], street2, fontsize=12, ha='right', color='black')
    return max_flow_value, fig, ax
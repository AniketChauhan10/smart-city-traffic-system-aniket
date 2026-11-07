
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from route_planner import dijkstra
from traffic_analysis import bellman_ford, simulate_congestion
from connectivity_module import bfs, dfs
from mst_planner import prim_mst, kruskal_mst


st.set_page_config(
    page_title="Smart City Traffic Management",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Smart City Traffic Management System")
st.write(
    "Plan routes, analyze traffic congestion, explore connectivity, "
    "and optimize road infrastructure."
)


# Create the sample city network
def create_city():
    graph = nx.Graph()

    roads = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3)
    ]

    for u, v, weight in roads:
        graph.add_edge(u, v, weight=weight)

    return graph


if "city_graph" not in st.session_state:
    st.session_state.city_graph = create_city()

city = st.session_state.city_graph
nodes = list(city.nodes())


# Draw the road network
def draw_graph(graph, highlighted_path=None):
    highlighted_path = highlighted_path or []

    positions = nx.spring_layout(graph, seed=42)

    fig, ax = plt.subplots(figsize=(9, 5))

    nx.draw_networkx(
        graph,
        positions,
        ax=ax,
        node_size=1400,
        node_color="lightblue",
        font_size=11
    )

    edge_labels = {
        (u, v): f"{data.get('weight', 1)} min"
        for u, v, data in graph.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        graph, positions, edge_labels=edge_labels, ax=ax
    )

    path_edges = list(zip(highlighted_path, highlighted_path[1:]))

    if path_edges:
        nx.draw_networkx_edges(
            graph,
            positions,
            edgelist=path_edges,
            edge_color="red",
            width=3,
            ax=ax
        )

    ax.set_title("City Road Network")
    ax.axis("off")
    return fig


# Network overview
st.subheader("1. Road Network Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Intersections", city.number_of_nodes())
col2.metric("Roads", city.number_of_edges())
col3.metric(
    "Connected",
    "Yes" if nx.is_connected(city) else "No"
)

st.pyplot(draw_graph(city))

with st.expander("View adjacency list and adjacency matrix"):
    adjacency_list = {
        node: list(city.neighbors(node))
        for node in city.nodes()
    }
    st.write("**Adjacency List**")
    st.json(adjacency_list)

    st.write("**Adjacency Matrix (road weights)**")
    matrix = nx.to_pandas_adjacency(
        city, nodelist=list(city.nodes()), weight="weight"
    )
    st.dataframe(matrix)


# Route planning
st.divider()
st.subheader("2. Route Planning")

if len(nodes) >= 2:
    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox(
            "Starting intersection",
            nodes,
            index=0,
            key="route_source"
        )

    with col2:
        destination = st.selectbox(
            "Destination intersection",
            nodes,
            index=len(nodes) - 1,
            key="route_destination"
        )

    algorithm = st.radio(
        "Choose route algorithm",
        ["Dijkstra", "Bellman-Ford"],
        horizontal=True
    )

    if st.button("Find Best Route"):
        try:
            if algorithm == "Dijkstra":
                path, distance, updates = dijkstra(
                    city, source, destination
                )
            else:
                path, distance, updates = bellman_ford(
                    city, source, destination
                )

            if path:
                st.success(f"Best route: {' → '.join(path)}")
                st.metric("Total travel time", f"{distance} minutes")
                st.pyplot(draw_graph(city, path))

                with st.expander("View algorithm updates"):
                    st.dataframe(pd.DataFrame(updates))
            else:
                st.warning("No route exists between these intersections.")

        except (ValueError, nx.NetworkXException) as error:
            st.error(str(error))


# Traffic congestion
st.divider()
st.subheader("3. Traffic Congestion Analysis")

roads = list(city.edges())

if roads:
    selected_road = st.selectbox(
        "Select a road to simulate congestion",
        roads,
        format_func=lambda edge: (
            f"{edge[0]} ↔ {edge[1]} "
            f"({city[edge[0]][edge[1]]['weight']} minutes currently)"
        )
    )

    new_weight = st.number_input(
        "New travel time (minutes)",
        min_value=0.1,
        value=float(city[selected_road[0]][selected_road[1]]["weight"] * 2),
        step=1.0
    )

    if st.button("Simulate Congestion"):
        try:
            updated_city = simulate_congestion(
                city,
                selected_road[0],
                selected_road[1],
                float(new_weight)
            )

            source = st.session_state.get("route_source", nodes[0])
            destination = st.session_state.get(
                "route_destination", nodes[-1]
            )

            old_path, old_cost, _ = bellman_ford(
                city, source, destination
            )
            new_path, new_cost, _ = bellman_ford(
                updated_city, source, destination
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Before congestion**")
                st.write(" → ".join(old_path) if old_path else "No route")
                st.write(f"Travel time: {old_cost} minutes")

            with col2:
                st.write("**After congestion**")
                st.write(" → ".join(new_path) if new_path else "No route")
                st.write(f"Travel time: {new_cost} minutes")

            st.pyplot(draw_graph(updated_city, new_path))

        except ValueError as error:
            st.error(str(error))


# Connectivity
st.divider()
st.subheader("4. Connectivity Analysis")

if nodes:
    start_node = st.selectbox(
        "Choose starting intersection for traversal",
        nodes,
        key="traversal_start"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Breadth-First Search (BFS)**")
        st.write(" → ".join(bfs(city, start_node)))

    with col2:
        st.write("**Depth-First Search (DFS)**")
        st.write(" → ".join(dfs(city, start_node)))

    st.write(
        "All intersections are reachable from the selected start: "
        + ("Yes" if nx.is_connected(city) else "No")
    )


# Minimum spanning tree
st.divider()
st.subheader("5. Road Infrastructure Optimization")

mst_algorithm = st.radio(
    "Choose MST algorithm",
    ["Prim's Algorithm", "Kruskal's Algorithm"],
    horizontal=True
)

if st.button("Calculate Minimum Spanning Tree"):
    try:
        if mst_algorithm == "Prim's Algorithm":
            mst_edges, total_cost = prim_mst(city)
        else:
            mst_edges, total_cost = kruskal_mst(city)

        st.success(f"Minimum infrastructure cost: {total_cost}")

        mst_graph = nx.Graph()
        mst_graph.add_nodes_from(city.nodes())

        for u, v, weight in mst_edges:
            mst_graph.add_edge(u, v, weight=weight)

        st.write("**Selected roads**")
        st.dataframe(
            pd.DataFrame(
                mst_edges,
                columns=["Intersection 1", "Intersection 2", "Cost"]
            )
        )

        st.pyplot(draw_graph(mst_graph))

    except ValueError as error:
        st.error(str(error))


st.caption(
    "Academic project | Design and Analysis of Algorithms Lab | "
    "BCA (AI & DS)"
)

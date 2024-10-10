import streamlit as st
from neo4j import GraphDatabase
from pyvis.network import Network
import tempfile
from neo4j import GraphDatabase

# Neo4j connection parameters
uri = "neo4j+s://184949f1.databases.neo4j.io"
username = "neo4j"
password = "OaXpt1ZNW3yqq4EvvzVTwJRPxm9C1YNhomaG8pnBu7I"

# Initialize Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=True)

# Function to run a Cypher query and fetch nodes and relationships
def fetch_graph_data(query):
    with driver.session() as session:
        result = session.run(query)
        nodes = set()
        edges = []
        for record in result:
            # Extracting nodes
            nodes.add(record["n1"]["name"])  # Assuming 'name' is a property of the nodes
            nodes.add(record["n2"]["name"])
            
            # Extracting relationships
            edges.append((record["n1"]["name"], record["n2"]["name"], record["rel"].type))
        
        return list(nodes), edges

# Function to create the graph visualization using Pyvis
def visualize_graph(nodes, edges):
    net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")

    # Add nodes
    for node in nodes:
        net.add_node(node, label=node)

    # Add edges (relationships)
    for edge in edges:
        source, target, relationship = edge
        net.add_edge(source, target, title=relationship)

    # Save graph as HTML in a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        return tmp_file.name

# Streamlit app layout
def main():
    st.title("Neo4j Knowledge Graph Visualization")

    # User input for Cypher query
    query = st.text_area("MATCH p=()-[]->() RETURN p LIMIT 25;", value="MATCH (n1)-[rel]->(n2) RETURN n1, n2, rel LIMIT 25")

    if st.button("Run Query"):
        try:
            nodes, edges = fetch_graph_data(query)
            if nodes and edges:
                st.success("Data fetched successfully! Rendering the graph...")

                # Visualize the graph
                graph_html = visualize_graph(nodes, edges)

                # Render the graph in Streamlit
                with open(graph_html, "r", encoding="utf-8") as file:
                    html_content = file.read()
                    st.components.v1.html(html_content, height=600)
            else:
                st.warning("No data found for the given query.")
        except Exception as e:
            st.error(f"Error fetching data: {e}")

if __name__ == "__main__":
    main()

from datetime import datetime, timezone
from classes import User, Post
import networkx as nx
import matplotlib.pyplot as plt

class SocialMediaGraph:
    def __init__(self):
        self.users = {} #  Dictionary to store users by user_id

    def add_user(self, user_id, **kwargs):
        """Adds a new user to the graph"""
        if user_id not in self.users:
            self.users[user_id] = User(user_id, **kwargs)

    def add_connections(self, user_id_1, user_id_2, connection_type):
        """Adds a direction connection between two users."""
        user1 = self.users.get(user_id_1)
        user2 = self.users.get(user_id_2)
        if user1 and user2:
            user1.add_connection(connection_type, user2)

    def filter_users(self, min_posts=None, max_posts=None, gender=None, country=None):
        """Filters users based on the specified criteria."""
        filtered_users = []
        for user in self.users.values():
            if min_posts is not None and len(user.authored_posts) < min_posts:
                continue
            if max_posts is not None and len(user.authored_posts) > max_posts:
                continue
            if gender and user.gender != gender:
                continue
            if country and user.country != country:
                continue
            filtered_users.append(user)
        return filtered_users
    
    def cluster_users(self, connection_type):
        """Clusters users based on a specific connection type."""
        visited = set()
        clusters = []

        def dfs(user, cluster):
            visited.add(user.user_id)
            cluster.append(user)
            for conn in user.connections_by_type(connection_type):
                connected_user = conn["user"]
                if connected_user.user_id not in visited:
                    dfs(connected_user, cluster)

        for user in self.users.values():
            if user.user_id not in visited:
                cluster = []
                dfs(user, cluster)
                clusters.append(cluster)

        return clusters
    
class SocialMediaVisualizer:
    def __init__(self, graph):
        self.graph = graph

    def draw_network(self, highlight_users=None, layout="spring"):
        """Draws the social network graph."""
        G = nx.DiGraph()

        # Add users and their connections
        for user in self.graph.users.values():
            G.add_node(user.user_id)
            for conn in user.connections:
                G.add_edge(user.user_id, conn["user"].user_id)

        # Apply layout
        if layout == "spring":
            pos = nx.spring_layout(G)
        elif layout == "circular":
            pos = nx.circular_layout(G)
        else:
            pos = nx.random_layout(G)

        # Draw the graph
        plt.figure(figsize=(12, 8))
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=500,
            node_color="lightblue",
            font_size=10,
            font_weight="bold",
        )

        # Highlight specific users if provided
        if highlight_users:
            nx.draw_networkx_nodes(
                G, pos, nodelist=highlight_users, node_color="orange", node_size=700
            )

        plt.title("Social Media Network Visualization")
        plt.show()

    def export_network(self, filepath="network.png"):
        """Exports the current graph visualization to a file."""
        G = nx.DiGraph()
        for user in self.graph.users.values():
            G.add_node(user.user_id)
            for conn in user.connections:
                G.add_edge(user.user_id, conn["user"].user_id)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue")
        plt.savefig(filepath)
        print(f"Graph exported to {filepath}")

"""Example Usage"""
# Initialize graph
social_graph = SocialMediaGraph()

# Add users
social_graph.add_user("u1", name="Alice", gender="F", age=30, country="USA")
social_graph.add_user("u2", name="Bob", gender="M", age=25, country="USA")
social_graph.add_user("u3", name="Charlie", gender="M", age=35, country="UK")

# Filter users
filtered_users = social_graph.filter_users(min_post=0, gender="M")
print("Filtered Users:", [user.name for user in filtered_users])

# Cluster users
clusters = social_graph.cluster_users("follows")
print("Clusters:", [[user.name for user in cluster] for cluster in clusters])

# Visualize the network
visualizer = SocialMediaVisualizer(social_graph)
visualizer.draw_network()
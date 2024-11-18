import networkx as nx
import matplotlib.pyplot as plt
from my_classes import User, Post

class SocialNetworkVisualizer:
    def __init__(self, users):
        self.users = users
        self.G = nx.Graph()
    
    def create_graph(self, importance_criteria='comments'):
        """Creates a graph with users, posts, and interactions."""
        self.G.clear()  # Clear existing graph
        
        # Add users as nodes
        for user in self.users:
            self.G.add_node(f"user_{user.user_id}", 
                           type='user', 
                           name=user.name,
                           label=user.name or f"User {user.user_id}")

        # Add posts and their connections
        for user in self.users:
            for post in user.authored_posts:
                post_id = f"post_{id(post)}"  # Unique identifier for post
                
                # Calculate importance
                importance = self.calculate_importance(post, importance_criteria)
                
                # Add post node
                self.G.add_node(post_id,
                              type='post',
                              content=post.content,
                              importance=importance,
                              label=post.content[:20] + "...")  # Truncated content as label
                
                # Add edge from author to post
                self.G.add_edge(f"user_{user.user_id}", post_id, 
                              relation='authored',
                              weight=2)  # Higher weight for authorship
                
                # Add edges for viewers
                for viewer in post.seen_by:
                    self.G.add_edge(f"user_{viewer.user_id}", post_id,
                                  relation='viewed',
                                  weight=1)  # Lower weight for views
        
        return self.G

    def calculate_importance(self, post, criteria):
        """Calculate post importance based on criteria."""
        if criteria == 'comments':
            return len(post.comments) * 100
        elif criteria == 'views':
            return len(post.seen_by) * 100
        elif criteria == 'combined':
            return (len(post.comments) + len(post.seen_by)) * 50
        return 0

    def visualize(self, importance_criteria='comments'):
        """Visualizes the network with highlighted important posts."""
        self.create_graph(importance_criteria)
        
        # Set up the layout
        pos = nx.spring_layout(self.G, k=1, iterations=50)
        
        # Prepare node attributes
        node_sizes = []
        node_colors = []
        labels = {}
        
        for node in self.G.nodes():
            node_data = self.G.nodes[node]
            labels[node] = node_data.get('label', '')
            
            if node_data['type'] == 'post':
                importance = node_data.get('importance', 0)
                node_sizes.append(1000 + importance)  # Base size + importance
                node_colors.append('lightblue')
            else:  # user node
                node_sizes.append(500)  # Fixed size for users
                node_colors.append('lightgreen')
        
        # Create the visualization
        plt.figure(figsize=(12, 8))
        
        # Draw edges
        nx.draw_networkx_edges(self.G, pos, alpha=0.2)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos, 
                             node_size=node_sizes,
                             node_color=node_colors)
        
        # Draw labels
        nx.draw_networkx_labels(self.G, pos, labels, font_size=8)
        
        plt.title(f"Social Network Visualization\nPost Importance by {importance_criteria.capitalize()}")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

# Example usage
def main():
    # Create users
    alice = User(1, "Alice")
    bob = User(2, "Bob")
    charlie = User(3, "Charlie")
    
    # Create posts
    post1 = Post(alice, "Alice's first post about data science")
    post2 = Post(bob, "Bob's thoughts on machine learning")
    post3 = Post(charlie, "Charlie's tutorial on Python")
    
    # Add comments
    post1.comments.extend(["Great post!", "Very informative", "Thanks for sharing"])
    post2.comments.extend(["Interesting perspective", "Well said"])
    post3.comments.append("This helped me a lot!")
    
    # Add views
    for post in [post1, post2, post3]:
        for user in [alice, bob, charlie]:
            user.add_read_post(post)
    
    # Create and run visualizer
    visualizer = SocialNetworkVisualizer([alice, bob, charlie])
    
    # Show different visualizations
    visualizer.visualize('comments')
    visualizer.visualize('views')
    visualizer.visualize('combined')

if __name__ == "__main__":
    main()
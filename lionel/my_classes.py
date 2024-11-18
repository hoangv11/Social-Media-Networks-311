class User:
    def __init__(self, user_id, name=None, gender=None, age=None, country=None, region=None):
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.age = age
        self.country = country
        self.region = region
        self.connections = []  # List of other User objects representing connections
        self.authored_posts = []  # List of Post objects authored by the user
        self.read_posts = []  # List of Post objects read by the user
        self.comments = []  # List of strings representing comments made by the user

    def add_connection(self, connection_type, connected_user):
        """Adds a connection to another user."""
        self.connections.append({
            "type": connection_type,
            "user": connected_user
        })
        self.connections.sort()

    def connections_by_type(self, connection_type=None):
        """Returns connections filtered by type if specified."""
        if connection_type is None:
            return self.connections
        return [conn for conn in self.connections if conn["type"] == connection_type]

    def add_read_post(self, post):
        """Adds a post to the list of read posts."""
        if post not in self.read_posts:
            self.read_posts.append(post)
            post.add_view(self)

class Post:
    def __init__(self, creator, content, responding_to=None, time_and_date=None):
        self.creator = creator  # User object who created the post
        self.content = content  # String representing the post's text
        self.responding_to = responding_to  # Post object this post responds to
        self.time_and_date = time_and_date  # Time and date of creation
        self.seen_by = []  # List of User objects who have seen the post
        self.comments = []  # List of comments on the post
        
        # Add this post to creator's authored posts
        creator.authored_posts.append(self)

    def add_view(self, user):
        """Adds a user's view to the post."""
        if user not in self.seen_by:
            self.seen_by.append(user)

    def add_comment(self, comment):
        """Adds a comment to the post."""
        self.comments.append(comment)

    def seen_by_age(self, min_age, max_age):
        """Returns list of users who have seen the post within the age range."""
        return [user for user in self.seen_by 
                if user.age and min_age <= user.age <= max_age]

    def seen_by_country_or_region(self, country=None, region=None):
        """Returns list of users who have seen the post from specified location."""
        if country:
            return [user for user in self.seen_by if user.country == country]
        elif region:
            return [user for user in self.seen_by if user.region == region]
        return []
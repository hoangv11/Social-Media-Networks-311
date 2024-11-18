class User:
    def __init__(self, user_id, name=None, gender=None, age=None, country=None, region=None):
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.age = age
        self.country = country
        self.region = region
        self.connections = []  # List of other User objects representing connections
        self.authored_posts = []  # List of strings, each representing a post authored by the user
        self.read_posts = []  # List of strings, each representing a post read by the user
        self.comments = []  # List of strings, each representing a comment made by the user

    def add_connection(self, connection_type, connected_user):
        """Adds a connection to another user."""
        self.connections.append({
            "type": connection_type,
            "user": connected_user
        })
        self.connections.sort()

    def connections_by_type(self, connection_type=None):
        """Returns connections filtered by type if specified."""
        if (type is None):
            return self.connections
        else:
            temp = [] #do not return all connections if not none
            for x in self.connections:
                if x.type == type:
                    temp.append(x)
            return temp

    def add_read_post(self, post):
        """Adds a post to the list of read posts."""
        self.read_posts.append(post)

class Post:
    def __init__(self, creator, content, responding_to=None, time_and_date=None, seen_by=[]):
        self.creator = creator  # User object who created the post
        self.content = content  # String representing the post's text
        self.responding_to = responding_to  # Post object this post responds to (if None, then this is not a Comment)
        self.time_and_date = time_and_date  # Time and date when the post was created (consider using datetime objects)
        self.seen_by = seen_by

    def add_view(self, user):
        """Adds a user's view to the post."""
        (self.seen_by).append(user.user_id)

    def seen_by_age(self, min, max):
        temp = []
        for x in self.seen_by:
            if (x.age <= max and x.age >= min):
                temp.append(x)
        return temp

    def seen_by_country_or_region(self, country, region=None):
        temp = []
        if region is None:
            for x in self.seen_by:
                if (x.creator.country == country):
                    temp.append(x)
        else:
            for x in self.seen_by:
                if (x.creator.region == region):
                    temp.append(x)
        return temp

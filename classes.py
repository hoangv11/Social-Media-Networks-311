class User:
    def __init__(self, user_id, name=None):
        self.user_id = user_id
        self.name = name
        self.connections = []
        self.authorized_posts = []
        self.read_posts = []
        self.comments = []
        
    def add_connection(self, connection_type, connected_user):
        self.connections.append({
            "type": connection_type,
            "user": connected_user
        })
        self.connections.sort()
        
    def connections_by_type(self, type=None):
        if (type is None):
            return self.connections
        else: 
            temp = []
            for x in self.connections:
                if x.type == type:
                    temp.append(x)
                return temp
            
class Post:
    def __init__(self, creator, content, responding_to=None, time_and_date=None, seen_by=[]):
        self.creator = creator
        self.content = content
        self.responding = responding_to
        self.time_and_date = time_and_date
        self.seen_by = seen_by
        
    def add_view(self, user):
        (self.seen_by).append(user.user_id)
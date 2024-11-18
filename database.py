import json
from classes import User, Post

class Database:
  def load_data(filename="social_network.json"):
      try:
          with open(filename, "r") as f:
              data = json.load(f)
          users = [User(**user) for user in data["users"]]
          posts = [Post(**post) for post in data["posts"]]
          return users, posts
      except FileNotFoundError:
          return [], []

  def save_data(users, posts, filename="social_network.json"):
      data = {
          "users": [user.to_dict() for user in users],
          "posts": [post.to_dict() for post in posts]
      }
      with open(filename, "w") as f:
          json.dump(data, f)


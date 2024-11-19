from wordcloud import WordCloud
from classes import User, Post
from generate_wordcloud import generate_wordcloud
import matplotlib.pyplot as plt
import re

def calculate_trending_score(post):
    """Calculate a simple trending score based on views."""
    return len(post.seen_by)

def generate_trending_report(posts, keywords=[], exclude_keywords=[], user_attributes=None):
    """Generate a report of trending posts with filtering options."""
    ranked_posts = sorted(posts, key=calculate_trending_score, reverse=True)
    for post in ranked_posts: 
        print(f"Post ID: {post.id}, Content: {post.content}, Author: {post.author.name}")

    wordcloud = generate_wordcloud(posts=posts, keywords=keywords, exclude_keywords=exclude_keywords, user_attributes=user_attributes)

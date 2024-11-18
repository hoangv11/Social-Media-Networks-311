from wordcloud import WordCloud
from classes import User, Post
import matplotlib.pyplot as plt
import re

def generate_wordcloud(users, posts, include_keywords=None, exclude_keywords=None, user_attributes=None):
    # Text storage for word cloud
    text = ""  

    # Filter users by attributes
    filtered_users = users
    if user_attributes:
        filtered_users = [
            user for user in users
            if all(getattr(user, attr, None) == value for attr, value in user_attributes.items())
        ]

    # Collect posts authored by filtered users
    filtered_posts = [
        post for post in posts
        if post.creator in filtered_users
    ]

    # Apply filters for keywords
    for post in filtered_posts:
        content = post.content.lower()
        if include_keywords and not any(keyword.lower() in content for keyword in include_keywords):
            continue
        if exclude_keywords and any(keyword.lower() in content for keyword in exclude_keywords):
            continue
        text += f" {content}"

    # Return if there are no words
    if not text.strip():
        print("No words to generate word cloud")
        return

    # Clean text
    text = re.sub(r'\W+', ' ', text) 

    # Generate Word Cloud
    wordcloud = WordCloud(
        background_color='white',
        width=1000,
        height=500
    ).generate(text)

    # Display the word cloud
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# Example Usage
if __name__ == "__main__":
    # Example users
    user1 = User(user_id=1, name="Alice", age=25, gender="female", country="USA", region="West")
    user2 = User(user_id=2, name="Bob", age=30, gender="male", country="USA", region="East")

    # Example posts
    post1 = Post(creator=user1, content="Social media trends are fascinating.")
    post2 = Post(creator=user2, content="Technology is shaping the future of social media.")
    post3 = Post(creator=user1, content="The impact of technology on society is immense.")

    # Add posts to a list
    posts = [post1, post2, post3]

    # Generate word cloud with filters
    generate_wordcloud(
        users=[user1, user2],
        posts=posts,
        include_keywords=["social", "technology"],
        exclude_keywords=["future"],
        user_attributes={"age": 25}
    )

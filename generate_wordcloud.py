from wordcloud import WordCloud
from classes import User, Post
import matplotlib.pyplot as plt
import re

def generate_word_cloud(users, posts, include_keywords=None, exclude_keywords=None, user_attributes=None):
    """
    Generates a word cloud based on the dataset and filters.

    Parameters:
        users (list): List of User objects.
        posts (list): List of Post objects.
        include_keywords (list): List of keywords to filter posts to include.
        exclude_keywords (list): List of keywords to filter posts to exclude.
        user_attributes (dict): Filters for user attributes (e.g., age, gender, region).

    Returns:
        None: Displays the word cloud or a message if no data matches the criteria.
    """
    combined_text = ""  # Text storage for word cloud

    # Filter users by attributes if provided
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

    # Apply keyword filters
    for post in filtered_posts:
        content = post.content.lower()
        if include_keywords and not any(keyword.lower() in content for keyword in include_keywords):
            continue
        if exclude_keywords and any(keyword.lower() in content for keyword in exclude_keywords):
            continue
        combined_text += f" {content}"

    # Check if there's any text to process
    if not combined_text.strip():
        print("No matching posts found. Unable to generate a word cloud.")
        return

    # Clean and preprocess the text
    combined_text = re.sub(r'\W+', ' ', combined_text)  # Remove special characters and punctuation

    # Generate the word cloud
    wordcloud = WordCloud(
        background_color='white',
        width=800,
        height=400
    ).generate(combined_text)

    # Display the word cloud
    plt.figure(figsize=(10, 6))
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
    generate_word_cloud(
        users=[user1, user2],
        posts=posts,
        include_keywords=["social", "technology"],
        exclude_keywords=["future"],
        user_attributes={"age": 25}
    )

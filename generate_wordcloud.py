from wordcloud import WordCloud
from classes import User, Post
import matplotlib.pyplot as plt
import re

def generate_wordcloud(users, posts, include_keywords=None, exclude_keywords=None, user_attributes=None):
    """
    Generate a word cloud from posts with specified filters.
    
    """
    # Convert keywords to lowercase for case-insensitive comparison
    include_keywords = [k.lower() for k in (include_keywords or [])]
    exclude_keywords = [k.lower() for k in (exclude_keywords or [])]
    
    # Filter users by attributes
    filtered_users = users
    if user_attributes:
        filtered_users = [
            user for user in users
            if all(getattr(user, attr) == value for attr, value in user_attributes.items())
        ]

    # Collect and filter posts
    text_contents = []
    for post in posts:
        if post.creator not in filtered_users:
            continue
            
        content = post.content.lower()
        
        # Check include keywords
        if include_keywords and not any(keyword in content for keyword in include_keywords):
            continue
            
        # Check exclude keywords
        if exclude_keywords and any(keyword in content for keyword in exclude_keywords):
            continue
            
        text_contents.append(content)

    # Return if no content matches filters
    if not text_contents:
        print("No content matches the specified filters")
        return None

    # Join all content with spaces and clean text
    text = " ".join(text_contents)
    text = re.sub(r'\W+', ' ', text)

    # Generate Word Cloud
    try:
        wordcloud = WordCloud(
            background_color='white',
            width=1000,
            height=500,
            min_font_size=10,
            max_font_size=100
        ).generate(text)

        # Display the word cloud
        plt.figure(figsize=(12, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
        
        return wordcloud
    except Exception as e:
        print(f"Error generating word cloud: {str(e)}")
        return None

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

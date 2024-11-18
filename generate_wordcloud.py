from wordcloud import WordCloud
from classes import User, Post
import matplotlib.pyplot as plt
import re

def generate_wordcloud(users, posts, include_keywords=None, exclude_keywords=None, user_attributes=None):
    """
    Generate a word cloud from filtered social media posts.

    Returns:
        WordCloud object if successful, None otherwise
    """
    # Convert keywords to sets for O(1) lookup
    include_keywords = {k.lower() for k in (include_keywords or [])}
    exclude_keywords = {k.lower() for k in (exclude_keywords or [])}
    
    # Filter users by attributes - store in set for O(1) lookup
    filtered_users = set()
    if user_attributes:
        filtered_users = {
            user for user in users
            if all(getattr(user, attr) == value for attr, value in user_attributes.items())
        }
    else:
        filtered_users = set(users)
            
    # Collect and filter posts while tracking word frequencies
    word_frequencies = {}
    for post in posts:
        if post.creator not in filtered_users:
            continue
            
        content = post.content.lower()
        
        # Apply keyword filters
        if include_keywords and not any(keyword in content for keyword in include_keywords):
            continue
        if exclude_keywords and any(keyword in content for keyword in exclude_keywords):
            continue
            
        # Count word frequencies
        words = content.split()
        for word in words:
            word = re.sub(r'\W+', '', word)  # Remove non-word characters
            if word:  # Skip empty strings
                word_frequencies[word] = word_frequencies.get(word, 0) + 1
    
    if not word_frequencies:
        print("No content matches the specified filters")
        return None

    # Generate word cloud from frequencies
    try:
        wordcloud = WordCloud(
            width=1000, 
            height=500,
            background_color='white',
            min_font_size=10,
            max_font_size=100
        ).generate_from_frequencies(word_frequencies)
        
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
        exclude_keywords=[],
        user_attributes={"age": 25}
    )

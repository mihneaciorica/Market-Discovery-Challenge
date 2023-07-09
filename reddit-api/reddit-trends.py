import requests
from textblob import TextBlob

# Set up API credentials and parameters
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
user_agent = 'Script_App'

def search_reddit_posts(keyword, subreddit='all', limit=500):
    posts = []
    headers = {'User-Agent': user_agent}
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={keyword}&limit={limit}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'children' in data['data']:
            for child in data['data']['children']:
                post = child['data']
                if(post['score'] > 500):
                    posts.append({'title': post['title'], 'author': post['author'], 'score': post['score'], 'id': post['id']})

    return posts

# So this function is the backbone since it returns posts based on keywords which in the case of our problem should be the business_tags that 
# the user inputs through user_input function -- check colab Market Discovery.ipynb 
# Now we have to take the posts and loop through each one of them, grab the id of the post through the api and feed this as iput to the 
#reddit-comments-from-post-trends.py


def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment

# below instead of passing post_id, should pass search_reddit_posts() as parameter , must loop through the returned posts 

def search_comments_in_post(post_id, keyword):
    comments = []
    headers = {'User-Agent': user_agent}
    url = f"https://www.reddit.com/comments/{post_id}.json"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 1:
            comment_tree = data[1]['data']['children']
            process_comment_tree(comment_tree, keyword, comments)

    return comments  # Also let's limit this to a decent nummber of comments 

def process_comment_tree(comment_tree, keyword, comments):
    for comment_item in comment_tree:
        comment_data = comment_item['data']
        if 'body' in comment_data and keyword.lower() in comment_data['body'].lower():
            sentiment = analyze_sentiment(comment_data['body'])
            comments.append({'body': comment_data['body'], 'author': comment_data['author'], 'score': comment_data['score'], 'sentiment': sentiment})

        if 'replies' in comment_data and comment_data['replies'] != '':
            if 'data' in comment_data['replies'] and 'children' in comment_data['replies']['data']:
                replies_data = comment_data['replies']['data']['children']
                process_comment_tree(replies_data, keyword, comments)

    found_comments = search_comments_in_post(post_id, keyword)

    # Display the found comments with sentiment analysis
    for comment in found_comments:
        # Add header before the comments' details
        print('Here are some reactions from people who are interested in your business ')
        print(f"Comment: {comment['body']}")
        print(f"Author: {comment['author']}")
        print(f"Score: {comment['score']}")
        print(f"Sentiment: {comment['sentiment']}")
        print('-' * 50)

# After making this work , please test with the business_tags from this company example: 

"""
company_name --- Tyfone
main_country --- United States
main_region --- Oregon
main_city --- Portland
main_latitude --- 45.484375
main_longitude --- -122.67596435546875
num_locations --- 1.0
company_type --- Private
year_founded --- 2004.0
employee_count --- 19.0
estimated_revenue --- 78500000.0
short_description --- At Tyfone, we understand that an elegant, engaging, intuitive user experience is the minimum requirement for any digital banking provider in today's market.
long_description --- At Tyfone, we understand that an elegant, engaging, intuitive user experience is the minimum requirement for any digital banking provider in today's market. What differentiates us is our unwavering commitment to exceptional collaboration and communication. We consider each customer a true partner and place the highest value on every relationship.
business_tags --- ['Mobile Banking', 'Partner Ecosystem', 'FinTech', 'Software Security', 'Cloud Engineers', 'Digital Banking Solutions', 'Digital Banking', 'Credit Union', 'Digital Transformation', 'Sales & Marketing']
business_model --- Services
product_type --- Professional Services
aggregated_industry --- Banks & Financial Services
main_business_category --- Banks & ATMs
main_industry --- Finance
main_sector --- IT&C Services
"""
                    
"""
Not needed as we would be running this on Colab, we need the function only

# Usage of the module
if __name__ == '__main__':
    # Example keyword to search for posts
    keyword = 'vr,ar'

    # Search for Reddit posts
    found_posts = search_reddit_posts(keyword)

    # Display the found posts
    for post in found_posts:
        print(f"Title: {post['title']}")
        print(f"Author: {post['author']}")
        print(f"Score: {post['score']}")
        print(f"ID: {post['id']}")
        print('-' * 50)
"""

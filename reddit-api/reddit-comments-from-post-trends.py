import requests
from textblob import TextBlob

# Set up API credentials and parameters
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
user_agent = 'Script_App'

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return sentiment

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

    return comments

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

# Usage of the module
if __name__ == '__main__':
    # Example post ID and keyword
    post_id = 'yl08zs'
    keyword = 'technology'

    # Search for comments in the post
    found_comments = search_comments_in_post(post_id, keyword)

    # Display the found comments with sentiment analysis
    for comment in found_comments:
        print(f"Comment: {comment['body']}")
        print(f"Author: {comment['author']}")
        print(f"Score: {comment['score']}")
        print(f"Sentiment: {comment['sentiment']}")
        print('-' * 50)

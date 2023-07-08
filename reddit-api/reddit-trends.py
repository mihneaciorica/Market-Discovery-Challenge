import requests

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

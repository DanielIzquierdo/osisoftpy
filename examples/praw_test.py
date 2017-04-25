import praw

#
#
# class BlazingReddit(object):
#     pass
#
# blazing = BlazingReddit()
#
# # blazing.auth = requests.auth.HTTPBasicAuth('4SqCF-YuaIvnyw', 'iHE8-MmrYYCeQqort1TvMZSwDpw')
# blazing.data = dict(grant_type='authorization_code',
#                     username='Hakaslak',
#                     password='oVB4Big957sSCJq5wS6JwCv8FHJUEfRSk6ouObFgjHBtnQwMZQoP72D0ngxFuw8e',
#                     user_agent='BlazingReddit/0.0.1 by Hakaslak')
#
# blazing.headers = {'User-Agent': 'BlazingReddit/0.0.1 by Hakaslak'}
#
# reddit_api = 'https://www.reddit.com/api/v1/access_token'
#
# # r = requests.post(reddit_api, auth=blazing.auth, data=blazing.data, headers=blazing.headers)
#
# # if r.status_code == requests.codes.ok:
# #     print('Connection OK')
# #     print(r.headers)
# #     print(r.json())
# #     print(r.access_token)
# # elif r.status_code != requests.codes.ok:
# #     r.raise_for_status()
# for submission in reddit.subreddit('android').hot(limit=5):
#     print(submission.title)

reddit = praw.Reddit(client_id='NRI1aQxwHKZkiQ',
                     client_secret="NNNyeXa4HGXSb2rTlwKqImHhYGY",
                     password='oVB4Big957sSCJq5wS6JwCv8FHJUEfRSk6ouObFgjHBtnQwMZQoP72D0ngxFuw8e',
                     user_agent='BlazingScriptForReddit', username='Hakaslak')

print(reddit.user.me())

for subreddit in reddit.subreddits.popular(limit=3):
    print(subreddit)
    for submission in subreddit.hot(limit=5):
        print(submission.title)

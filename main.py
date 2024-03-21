import os
from dotenv import load_dotenv
from openai import OpenAI
import praw
# reddit wrapper


load_dotenv()

client = OpenAI()
client_id=os.getenv('REDDIT_CLIENT_ID')
secret_key=os.getenv('REDDIT_SECRET_KEY')

def get_titles_and_comments(subreddit="stocks", limit=6, num_comments=3, skip_first=2):
    # skip_first is to skip the pinned posts
    subreddit = reddit.subreddit(subreddit)
    # Dictionary
    title_and_comments = {}

    for counter, post in enumerate(subreddit.hot(limit=limit)):
        if counter < skip_first:
            continue
        counter += (1-skip_first)

        title_and_comments[counter] = ""
        submission = reddit.submission(post.id)
        title = post.title

        # {0: 'Title: Post Title \n\n Comments: \n\n'}
        title_and_comments[counter] += 'Title: '+title+"\n\n"
        title_and_comments[counter] += 'Comments: \n\n'

        comment_counter = 0
        for comment in submission.comments:
            if not comment.body == '[deleted]':
                title_and_comments[counter] += comment.body+"\n"
                comment_counter += 1
            if comment_counter == num_comments:
                break
    return title_and_comments

def create_prompt(title_and_comments):
    task = "Return the stock ticker or company name mentioned in the following title and comments and classify the sentiment around the company as positive, negative, or natural If no tikcker or company is mentioned write 'No company mentioned'\n\n"
    return task + title_and_comments

if __name__ == '__main__':
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=secret_key,
                         user_agent="sentiment analysis test")

    # for submission in reddit.subreddit("stocks").hot(limit=5):
    #     # print(submission.title)     reddit.com/r/stocks

    # subreddit_stocks = reddit.subreddit("stocks")

    # for post in subreddit_stocks.hot(limit=5):
    #     print(post.title)
    #     submission = reddit.submission(post.id)
    #     # Print top 2 comments per title submission
    #     counter = 0
    #     for comment in submission.comments:
    #         if comment.body == '[deleted]':
    #             pass
    #         print(comment.body)
    #         counter+=1
    #         if counter == 2:
    #             break

    titles_and_comments = get_titles_and_comments()
    # print(create_prompt(titles_and_comments[1]))

    for key, title_with_comments in titles_and_comments.items():
        prompt = create_prompt(title_with_comments)

        response = client.completions.create(model='davinci-002',
                                             prompt=prompt,
                                             max_tokens=256,
                                             temperature=0,
                                             top_p=1.0,
                                             )

        print(title_with_comments)
        print(f"Sentiment Report from OpenAI: {response.choices[0].text}")
        print("-------------------------------------")
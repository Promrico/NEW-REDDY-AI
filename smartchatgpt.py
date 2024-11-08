import praw
import openai
import time
import random

# Load keywords from the text file
def load_keywords(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Load subreddits from the text file
def load_subreddits(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Reddit API credentials
reddit = praw.Reddit(
    client_id='yourclientid',
    client_secret='yourclientsecret',
    refresh_token='yourREFRESHtoken',
    user_agent='your user agent'
)

# OpenAI API key
openai.api_key = 'your chat gpt key'
# Load keywords and subreddits
keywords = load_keywords('keywords.txt')
subreddits = load_subreddits('subreddit.txt')

# Dictionary to track comments per post and per subreddit
comment_count = {}
subreddit_comment_count = {subreddit: 0 for subreddit in subreddits}

# Function to generate a comment using GPT-3.5-turbo
def generate_comment(post_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": post_text},
            {"role": "system", "content": "What are your thoughts on this topic? explain in between 20 to 75 words. And please mention my website name 'loopearplugs' exact same name. and dont mention www. and .com or anything with website name this is my website desciption. we sell best quality ear plugs for a good sleep. and plz answer with a wity humor. and first understand the post and if you think than you should mention our websit name"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Function to process posts in a subreddit
def process_subreddit(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    post_count = 0  # Track the number of fetched posts
    for submission in subreddit.new(limit=200):  # Fetch up to 200 new posts
        post_count += 1
        print(f"Fetched post: {submission.title}")
        if any(keyword.lower() in (submission.title + submission.selftext).lower() for keyword in keywords):
            print(f"Keyword found in post: {submission.title}")
            if subreddit_comment_count[subreddit_name] >= 3:
                break
            if submission.id not in comment_count:
                post_text = submission.title + "\n\n" + submission.selftext
                comment_text = generate_comment(post_text)
                submission.reply(comment_text)
                print(f"Replied to post: {submission.title}")
                comment_count[submission.id] = 1
                subreddit_comment_count[subreddit_name] += 1
                sleep_duration = random.randint(600, 750)  # Sleep between 10 to 12.5 minutes
                print(f"Sleeping for {sleep_duration} seconds")
                time.sleep(sleep_duration)
        else:
            print(f"No keyword found in post: {submission.title}")
        
        # Check if fetched enough posts or comments
        if post_count >= 200 or subreddit_comment_count[subreddit_name] >= 3:
            break

    print(f"Finished processing subreddit: {subreddit_name}")

# Main function to run the bot
def run_bot():
    for subreddit_name in subreddits:
        print(f"Processing subreddit: {subreddit_name}")
        process_subreddit(subreddit_name)
    print("Sleeping for 24 hours")
    time.sleep(86400)  # Sleep for 24 hours (86400 seconds)

# Run the bot
if __name__ == "__main__":
    while True:
        try:
            run_bot()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Sleep for 1 minute before retrying on error

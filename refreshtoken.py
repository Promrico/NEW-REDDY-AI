import praw

# Initialize PRAW without a refresh token to obtain it manually
reddit = praw.Reddit(
    client_id='FMZcGVDumBIYMz488ALJlA',  # Your client ID
    client_secret='hpR63Cuu0eBWwNRXkAAzHGZM2J317w',  # Your client secret
    redirect_uri='http://localhost:8080',  # or a suitable redirect URI
    user_agent='linux:REDDI.ai:v1.5.2 (by u/Fun_Practice_5369)'  # Custom user agent
)

# Print authorization URL for manual authentication (add more scopes if needed)
print(f"Visit this URL to authorize your app: {reddit.auth.url(['identity', 'read', 'submit'], '...', 'permanent')}")

# Once authorized, Reddit will redirect to your redirect URI with the code in the URL
auth_code = input("Enter the authorization code: ")

# Use the authorization code to generate a refresh token
refresh_token = reddit.auth.authorize(auth_code)

# Print and save the refresh token
print(f"Your refresh token: {refresh_token}")

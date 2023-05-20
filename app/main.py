from __init__ import create_app, db
from threading import Thread

app = create_app()  # Initialize the Flask app

# Create a separate thread for the fetch_mentions loop
def fetch_mentions_thread():
    with app.app_context():
        # Access the RedditBot instance from the app context
        reddit_bot = app.reddit_bot

        # Continuously fetch mentions
        for mention, post, user_req, user_settings in reddit_bot.fetch_mentions():
            # Process the mention and generate a reply
            explanation = app.openai_bot.generate_explanation(
                post.title, post.selftext, mention.subreddit.display_name, user_comment=user_req, settings=user_settings
            )
            
            # Reply to the mention
            reddit_bot.reply_to_post(mention, explanation)

# Start the fetch_mentions thread
fetch_mentions_thread = Thread(target=fetch_mentions_thread)
fetch_mentions_thread.start()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the SQLite database
    app.run(debug=True)  # Run the Flask app on debug mode
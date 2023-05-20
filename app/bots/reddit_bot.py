import praw
from models import User
from __init__ import db

class RedditBot:
    def __init__(self, client_id, client_secret, user_agent, username, password):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )
        self.db = db
        
    def fetch_mentions(self):
        """
        Yield new mentions of the bot.
        """
        for mention in praw.models.util.stream_generator(self.reddit.inbox.mentions):
            if not mention.new:  
                continue
            # Mark the mention as read so we don't process it again
            mention.mark_read()

            # Print the author of the mention
            if mention.author is not None:
                print(f"GPTBot was tagged by: {mention.author.name} on subreddit: {mention.subreddit.display_name}")
                print("---------------------------------------------")

                # Check if user exists in database
                reddit_username = mention.author.name
                user = self.db.session.query(User).filter_by(reddit_user=reddit_username).first()
                user_settings = None
                if user:
                    print(f"{user} found in database!")
                    print("---------------------------------------------")
                    # User exists, retrieve their settings
                    user_settings = {
                        'max_sentence': user.max_sentence,
                        'tone': user.tone,
                        'additional': user.additional,
                    }
            else:
                print("GPTBot was tagged by a deleted or suspended user.")
                print("---------------------------------------------")

            # Get the post that the bot was mentioned in
            post = self.reddit.submission(id=mention.submission.id)
            print(f"Title of Post: {post.title}")
            print("---------------------------------------------")
            print(f"Content of Post: {post.selftext}")
            print("---------------------------------------------")

            # user request but remove tag
            user_req = mention.body.replace("u/RedditGPTBot", "")
            print(f"User's Request: {user_req}")
            print("---------------------------------------------")
            yield mention, post, user_req, user_settings  # Include user settings in yield
            
    def reply_to_post(self, mention, message):
        """
        Reply to the given post with the given message.
        """
        print("Replying with: " + message)
        print("---------------------------------------------")
        mention.reply(message)
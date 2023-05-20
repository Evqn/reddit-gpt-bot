from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import OPENAI_API_KEY, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, REDDIT_USERNAME, REDDIT_PASSWORD



# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__) # creates the Flask instance, __name__ is the name of the current Python module
    app.config['SECRET_KEY'] = 'secret-key-goes-here' # it is used by Flask and extensions to keep data safe
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #it is the path where the SQLite database file will be saved
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # deactivate Flask-SQLAlchemy track modifications
    
    db.init_app(app) # Initialize sqlite database

    # The login manager contains the code that lets your application and Flask-Login work together
    login_manager = LoginManager() # Create a Login Manager instance
    login_manager.login_view = 'auth.login' # define the redirection path when login required and we attempt to access without being logged in
    login_manager.init_app(app) # configure it for login
    
    from models import User
    @login_manager.user_loader
    def load_user(user_id): #reload user object from the user ID stored in the session
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    # blueprint for auth routes in our app
    # blueprint allow you to orgnize your flask app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # blueprint for non-auth parts of app
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Initialize the bots
    from bots.reddit_bot import RedditBot
    from bots.openai_bot import OpenAIBot
    app.reddit_bot = RedditBot(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD
    )
    app.openai_bot = OpenAIBot(api_key=OPENAI_API_KEY)

    return app
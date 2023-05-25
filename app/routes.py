from flask import render_template
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import User
from __init__ import db

# our main blueprint
main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    # This is an example, replace with how you actually get your settings
    settings = [
        {'name': 'Reddit User', 'value': current_user.reddit_user},
        {'name': 'Max Sentence', 'value': current_user.max_sentence},
        {'name': 'Tone', 'value': current_user.tone},
        {'name': 'Custom Prompt', 'value': current_user.additional},
    ]
    return render_template('profile.html', name=current_user.name, settings=settings)


@main.route('/save_setting', methods=['POST'])
@login_required
def save_setting():
    setting_name = request.form.get('setting_name')
    setting_value = request.form.get('setting_value')

    if setting_name == 'Reddit User':
        current_user.reddit_user = setting_value
    elif setting_name == 'Max Sentence':
        current_user.max_sentence = setting_value
    elif setting_name == 'Tone':
        current_user.tone = setting_value
    elif setting_name == 'Additional':
        current_user.additional = setting_value

    db.session.commit()
    flash('Settings updated successfully.')
    return '', 200
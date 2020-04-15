from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
from project.models import Post

main = Blueprint('main', __name__)

@main.route('/')
def index():
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts)

@main.route('/', methods=['POST'])
def create_post():
    title = request.form['post-title']
    content = request.form['post-content']
    subreddit = request.form['subreddit']
    if subreddit == 'Music':
        subreddit_id = 0
    elif subreddit == 'Funny':
        subreddit_id = 1
    elif subreddit == 'Programming':
        subreddit_id = 2
    elif subreddit == 'News':
        subreddit_id = 3
    elif subreddit == 'Design':
        subreddit_id = 4
    else:
        subreddit_id = 5 

    sub = subreddit
    newPost = Post(title=title, description=content, sub=sub, votes=0, user=current_user, subreddit_id=subreddit_id)
    db.session.add(newPost)
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', name=current_user.name, all_posts=all_posts)    

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

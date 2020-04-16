from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
from project.models import Post, Subreddit

main = Blueprint('main', __name__)

@main.route('/')
def index():
    all_posts = Post.query.all()
    subreddits = Subreddit.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits)

@main.route('/upvote_post/<post_id>')
def upvote_post(post_id):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits)

@main.route('/downvote_post/<post_id>')
def downvote_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    subreddits = Subreddit.query.all()
    post.votes = post.votes - 1
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits)

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

    subreddits = Subreddit.query.all()
    sub = subreddit
    newPost = Post(title=title, description=content, sub=sub, votes=0, user=current_user, subreddit_id=subreddit_id)
    db.session.add(newPost)
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', name=current_user.name, all_posts=all_posts, subreddits=subreddits)    

@main.route('/subreddits/<sub_id>')
def get_posts_for_subreddit(sub_id):
    subreddits = Subreddit.query.all()
    sub_id = int(sub_id) 
    print('sub_id: ', sub_id)
    print('type(sub_id): ', type(sub_id))
    music_posts = Post.query.filter_by(subreddit_id=sub_id-1)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, subreddit_id=sub_id)

@main.route('/all')
def get_all_posts():
    subreddits = Subreddit.query.all()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits)

@main.route('/upvote_post_subreddit/<subreddit_id>/<post_id>')
def upvote_post_subreddit(post_id, subreddit_id):
    print('post_id: ', post_id)
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    sub_id = int(subreddit_id)
    sub_id = sub_id - 1
    print('sub_id: ', sub_id)
    music_posts = Post.query.filter_by(subreddit_id=sub_id)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, subreddit_id=sub_id+1)

@main.route('/downvote_post_subreddit/<subreddit_id>/<post_id>')
def downvote_post_subreddit(post_id, subreddit_id):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes - 1
    db.session.commit()
    sub_id = int(subreddit_id)
    sub_id = sub_id - 1
    print('sub_id: ', sub_id)
    music_posts = Post.query.filter_by(subreddit_id=sub_id)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, subreddit_id=sub_id+1)

@main.route('/profile<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('profile.html', user_posts=user_posts, name=current_user.name)


from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
from project.models import Post, Subreddit, User, Comment

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

@main.route('/subreddits/<sub_name>')
def get_posts_for_subreddit(sub_name):
    subreddits = Subreddit.query.all()
    music_posts = Post.query.filter_by(sub=sub_name)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, sub_name=sub_name)

@main.route('/all')
def get_all_posts():
    subreddits = Subreddit.query.all()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits)

@main.route('/upvote_post_subreddit/<sub_name>/<post_id>')
def upvote_post_subreddit(post_id, sub_name):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    music_posts = Post.query.filter_by(sub=sub_name)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, sub_name=sub_name)

@main.route('/downvote_post_subreddit/<sub_name>/<post_id>')
def downvote_post_subreddit(post_id, sub_name):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes - 1
    db.session.commit()
    music_posts = Post.query.filter_by(sub=sub_name)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, sub_name=sub_name)

@main.route('/profile<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=user_id)
    current_user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('profile.html', user_posts=user_posts, name=current_user.name, subreddits=subreddits)

@main.route('/upvote_post_profile/<user_id>/<post_id>')
def upvote_post_profile(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('profile.html', user_posts=user_posts, subreddits=subreddits, name=current_user.name)

@main.route('/downvote_post_profile/<user_id>/<post_id>')
def downvote_post_profile(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes - 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('profile.html', user_posts=user_posts, subreddits=subreddits, name=current_user.name)

@main.route('/post_details/<post_id>', methods=['GET', 'POST'])
def post_details(post_id):
    subreddits = Subreddit.query.all()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    print('target_post: ', target_post)
    return render_template('post_details.html', post=target_post, name=current_user.name, subreddits=subreddits)

@main.route('/create_comment/<post_id>/<user_id>', methods=['POST'])
def create_comment(post_id, user_id):
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    subreddits = Subreddit.query.all()
    text = request.form['comment-text']
    post_id = post_id
    user_id = user_id
    author = current_user.name
    author_id = current_user.id
    new_comment = Comment(text=text, post_id=post_id, user_id=user_id, author=author)
    comments = Comment.query.filter_by(post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    return render_template('post_details.html', post=target_post, name=current_user.name, subreddits=subreddits, comments=comments, author_id=author_id)

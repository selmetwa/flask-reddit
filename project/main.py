from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
from project.models import Post, Subreddit, User, Comment
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    all_posts = Post.query.all()
    subreddits = Subreddit.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits, profile=False, page_name='home')

@main.route('/upvote_post/<post_id>')
@login_required
def upvote_post(post_id):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits, profile=False, page_name='home')

@main.route('/downvote_post/<post_id>')
@login_required
def downvote_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    subreddits = Subreddit.query.all()
    post.votes = post.votes - 1
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits, page_name='home')

@main.route('/', methods=['POST'])
@login_required
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

    time = datetime.now()
    newtime = datetime.strftime(time, '%d/%m/%Y')
    print('newtime: ', newtime)
    print('time: ', time)
    print('newtime: ', type(newtime))
    subreddits = Subreddit.query.all()
    sub = subreddit
    newPost = Post(title=title, description=content, sub=sub, votes=0, user=current_user, subreddit_id=subreddit_id, timestamp=newtime)
    db.session.add(newPost)
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', name=current_user.name, all_posts=all_posts, subreddits=subreddits, profile=False, page_name='home')    

@main.route('/delete_post/<post_id>/<user_id>', methods=['GET'])
def delete_post(post_id, user_id):
    target_post = Post.query.filter_by(id=post_id).first_or_404()    
    print('post: ', target_post)
    db.session.delete(target_post)
    db.session.commit()
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=user_id)
    current_user = User.query.filter_by(id=user_id).first_or_404()
    list_of_posts = list(user_posts)
    user_comments = Comment.query.filter_by(user_id=user_id)
    list_of_comments = list(user_comments)
    return render_template('user.html', user_posts=user_posts,user_comments=user_comments, name=current_user.name, subreddits=subreddits, page_name=current_user.name, list_of_posts=list_of_posts, list_of_comments=list_of_comments)

@main.route('/subreddits/<sub_name>')
def get_posts_for_subreddit(sub_name):
    subreddits = Subreddit.query.all()
    music_posts = Post.query.filter_by(sub=sub_name)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, sub_name=sub_name, page_name=sub_name)

@main.route('/all')
def get_all_posts():
    subreddits = Subreddit.query.all()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits)

@main.route('/upvote_post_subreddit/<sub_name>/<post_id>')
@login_required
def upvote_post_subreddit(post_id, sub_name):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    music_posts = Post.query.filter_by(sub=sub_name)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, sub_name=sub_name, page_name=sub_name)

@main.route('/downvote_post_subreddit/<sub_name>/<post_id>')
@login_required
def downvote_post_subreddit(post_id, sub_name):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes - 1
    db.session.commit()
    music_posts = Post.query.filter_by(sub=sub_name)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, sub_name=sub_name,page_name=sub_name)

@main.route('/profile<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=user_id)
    current_user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('profile.html', user_posts=user_posts, name=current_user.name, subreddits=subreddits, profile=True, page_name=current_user.name)

@main.route('/user/<user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=user_id)
    list_of_posts = list(user_posts)
    user_comments = Comment.query.filter_by(user_id=user_id)
    list_of_comments = list(user_comments)
    current_user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user.html', user_posts=user_posts, user_comments=user_comments, name=current_user.name, subreddits=subreddits, page_name=current_user.name, list_of_posts=list_of_posts, list_of_comments=list_of_comments)

@main.route('/upvote_post_user/<user_id>/<post_id>')
@login_required
def upvote_post_user(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    list_of_posts = list(user_posts)
    user_comments = Comment.query.filter_by(user_id=user_id)
    list_of_comments = list(user_comments)
    return render_template('user.html', user_posts=user_posts,user_comments=user_comments, subreddits=subreddits, name=current_user.name, page_name=current_user.name, list_of_posts=list_of_posts, list_of_comments=list_of_comments)

@main.route('/downvote_post_user/<user_id>/<post_id>')
@login_required
def downvote_post_user(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes - 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    list_of_posts = list(user_posts)
    user_comments = Comment.query.filter_by(user_id=user_id)
    list_of_comments = list(user_comments)
    return render_template('user.html', user_posts=user_posts,user_comments=user_comments, subreddits=subreddits, name=current_user.name, page_name=current_user.name, list_of_posts=list_of_posts, list_of_comments=list_of_comments)

@main.route('/upvote_post_profile/<user_id>/<post_id>')
def upvote_post_profile(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('profile.html', user_posts=user_posts, subreddits=subreddits, name=current_user.name, profile=True, page_name=current_user.name)

@main.route('/downvote_post_profile/<user_id>/<post_id>')
def downvote_post_profile(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes - 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('profile.html', user_posts=user_posts, subreddits=subreddits, name=current_user.name, profile=True, page_name=current_user.name)

@main.route('/post_details/<post_id>', methods=['GET', 'POST'])
def post_details(post_id):
    subreddits = Subreddit.query.all()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id)
    print('target_post: ', target_post)
    return render_template('post_details.html', post=target_post, name=current_user.name, subreddits=subreddits, comments=comments)

@main.route('/upvote_post_details/<user_id>/<post_id>')
def upvote_post_details(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id)
    target_post.votes = target_post.votes + 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('post_details.html', post=target_post, subreddits=subreddits, comments=comments)

@main.route('/downvote_post_details/<user_id>/<post_id>')
def downvote_post_details(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id)
    target_post.votes = target_post.votes - 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('post_details.html', post=target_post, subreddits=subreddits, comments=comments)

@main.route('/create_comment/<post_id>/<user_id>', methods=['POST'])
def create_comment(post_id, user_id):
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    subreddits = Subreddit.query.all()
    text = request.form['comment-text']
    post_id = post_id
    user_id = user_id
    author_id = User.query.filter_by(name=current_user.name).first_or_404().id
    author = User.query.filter_by(id=user_id).first_or_404().name
    print('author: ', author)
    time = datetime.now()
    newtime = datetime.strftime(time, '%d/%m/%Y')
    new_comment = Comment(text=text, post_id=post_id, user_id=user_id, author=author, votes=0, timestamp=newtime)
    comments = Comment.query.filter_by(post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    return render_template('post_details.html', post=target_post, name=current_user.name, subreddits=subreddits, comments=comments)

@main.route('/upvote_comment/<user_id>/<post_id>/<comment_id>')
def upvote_comment(post_id, user_id, comment_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    target_comment = Comment.query.filter_by(id=comment_id).first_or_404()
    print('target_comment: ', target_comment)
    comments = Comment.query.filter_by(post_id=post_id)
    target_comment.votes = target_comment.votes + 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('post_details.html', post=target_post, subreddits=subreddits, comments=comments)

@main.route('/downvote_comment/<user_id>/<post_id>/<comment_id>')
def downvote_comment(post_id, user_id, comment_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    target_comment = Comment.query.filter_by(id=comment_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id)
    target_comment.votes = target_comment.votes - 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('post_details.html', post=target_post, subreddits=subreddits, comments=comments)

@main.route('/create_post_form', methods=['GET'])
@login_required
def create_post_form():
    return render_template('form.html')

@main.route('/edit_post_form/<user_id>/<post_id>', methods=['GET'])
def edit_post_form(user_id, post_id):
    print('user_id: ', post_id)
    print('post_id: ', user_id)
    post_to_edit = Post.query.filter_by(id=user_id).first_or_404()
    print('post_to_edit: ', post_to_edit)
    return render_template('edit_post_form.html', post_id=post_id, user_id=user_id, post_to_edit=post_to_edit)

@main.route('/edit_post/<post_id>/<user_id>', methods=['POST'])
def edit_post(post_id, user_id):
    post_to_edit = Post.query.filter_by(id=user_id).first_or_404()
    if request.form['btn'] == 'update':
        new_title = request.form['new-post-title']
        new_content = request.form['new-post-content'] 
        post_to_edit.title = new_title
        post_to_edit.description = new_content
        db.session.commit()
    else:
        pass
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=post_id)
    list_of_posts = list(user_posts)
    user_comments = Comment.query.filter_by(user_id=user_id)
    list_of_comments = list(user_comments)
    return render_template('user.html', user_posts=user_posts,user_comments=user_comments, subreddits=subreddits, name=current_user.name, page_name=current_user.name, list_of_posts=list_of_posts, list_of_comments=list_of_comments)

@main.route('/delete_comment/<comment_id>/<user_id>/<post_id>', methods=['GET'])
def delete_comment(comment_id, user_id, post_id):
    current_user = User.query.filter_by(id=user_id).first_or_404()
    target_comment = Comment.query.filter_by(id=comment_id).first_or_404()
    db.session.delete(target_comment)
    db.session.commit()
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=user_id)
    current_user = User.query.filter_by(id=user_id).first_or_404()
    list_of_posts = list(user_posts)
    user_comments = Comment.query.filter_by(user_id=user_id)
    list_of_comments = list(user_comments)
    return render_template('user.html', user_posts=user_posts,user_comments=user_comments, name=current_user.name, subreddits=subreddits, page_name=current_user.name, list_of_posts=list_of_posts, list_of_comments=list_of_comments, just_modified_comment=True)

@main.route('/edit_comment_form/<comment_id>/<user_id>/<post_id>', methods=['GET'])
def edit_comment_form(comment_id, user_id, post_id):
    print('user_id: ', post_id)
    print('post_id: ', user_id)
    comment_to_edit = Comment.query.filter_by(id=comment_id).first_or_404()
    return render_template('edit_comment_form.html', post_id=post_id, user_id=user_id, comment_id=comment_id, comment_to_edit=comment_to_edit)

@main.route('/edit_comment/<comment_id>/<user_id>/<post_id>', methods=['POST'])
def edit_comment(comment_id, user_id, post_id):
    comment_to_edit = Comment.query.filter_by(id=comment_id).first_or_404()
    print(' comment_to_edit: ',  comment_to_edit)
    if request.form['comment-btn'] == 'update':
        new_content = request.form['new-comment-content'] 
        comment_to_edit.text = new_content
        db.session.commit()
    else:
        pass
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=user_id)
    list_of_posts = list(user_posts)
    user_comments = Comment.query.filter_by(user_id=user_id)
    list_of_comments = list(user_comments)
    return render_template('user.html', user_posts=user_posts,user_comments=user_comments, subreddits=subreddits, name=current_user.name, page_name=current_user.name, list_of_posts=list_of_posts, list_of_comments=list_of_comments, just_modified_comment=True)

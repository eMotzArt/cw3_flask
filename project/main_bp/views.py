import random

from flask import render_template, Blueprint, request, url_for, redirect, jsonify
from project.globals import STATIC_PATH_ABS
from project.classes import UserIDentifier
from project.classes import Repository

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='./templates', static_folder=STATIC_PATH_ABS)

@main_blueprint.get('/')
def page_index():
    if not UserIDentifier().is_user_registered(request):
        return redirect(url_for('reg_blueprint.page_reg'), code=302)

    user_id = UserIDentifier().get_user_id(request)

    all_posts = Repository().get_all_posts()
    user_bookmarks = Repository().get_user_bookmarks(user_id)
    user_likes = Repository().get_user_likes(user_id)
    return render_template('index.html', posts=all_posts, bookmarks=user_bookmarks, likes=user_likes)

@main_blueprint.get('/search')
def page_search():
    if not UserIDentifier().is_user_registered(request):
        return redirect(url_for('reg_blueprint.page_reg'), code=302)

    user_id = UserIDentifier().get_user_id(request)
    user_bookmarks = Repository().get_user_bookmarks(user_id)
    user_likes = Repository().get_user_likes(user_id)

    search_line = request.args.get('search_line')
    posts_by_search_line = Repository().get_posts_by_search_line(search_line)


    return render_template('index.html', posts=posts_by_search_line, bookmarks=user_bookmarks, likes=user_likes, search=True)

@main_blueprint.get('/post/<int:post_id>')
def page_post(post_id):
    if not UserIDentifier().is_user_registered(request):
        return redirect(url_for('reg_blueprint.page_reg'), code=302)

    user_id = UserIDentifier().get_user_id(request)
    user_bookmarks = Repository().get_user_bookmarks(user_id)
    user_likes = Repository().get_user_likes(user_id)

    Repository().set_views_counter(post_id)

    post_by_id = Repository().get_post_by_id(post_id)
    comments_by_post_id = Repository().get_comments_by_post_id(post_id)
    return render_template('post.html', post=post_by_id, likes=user_likes, bookmarks=user_bookmarks, comments=comments_by_post_id)
    pass

@main_blueprint.get('/user/<user_name>')
def page_user(user_name):
    if not UserIDentifier().is_user_registered(request):
        return redirect(url_for('reg_blueprint.page_reg'), code=302)

    user_id = UserIDentifier().get_user_id(request)
    user_bookmarks = Repository().get_user_bookmarks(user_id)
    user_likes = Repository().get_user_likes(user_id)

    posts_by_user = Repository().get_posts_by_user_name(user_name)

    return render_template('user-feed.html', user_name=user_name, posts=posts_by_user, likes=user_likes, bookmarks=user_bookmarks)

@main_blueprint.get('/tag/<tag_name>')
def page_tag(tag_name):
    if not UserIDentifier().is_user_registered(request):
        return redirect(url_for('reg_blueprint.page_reg'), code=302)

    user_id = UserIDentifier().get_user_id(request)
    user_bookmarks = Repository().get_user_bookmarks(user_id)
    user_likes = Repository().get_user_likes(user_id)

    posts_by_tag = Repository().get_posts_by_tag(tag_name)
    return render_template('tag.html', tag_name=tag_name, posts=posts_by_tag, likes=user_likes, bookmarks=user_bookmarks)

@main_blueprint.get('/bookmarks')
def page_bookmarks():
    if not UserIDentifier().is_user_registered(request):
        return redirect(url_for('reg_blueprint.page_reg'), code=302)

    user_id = UserIDentifier().get_user_id(request)
    user_bookmarks = Repository().get_user_bookmarks(user_id)
    user_likes = Repository().get_user_likes(user_id)

    user_bookmarked_posts = Repository().get_posts_by_user_bookmarks(user_bookmarks)
    return render_template('bookmarks.html', posts=user_bookmarked_posts, likes=user_likes, bookmarks=user_bookmarks)

#add post
@main_blueprint.get('/add_post')
@main_blueprint.post('/add_post')
def add_post():
    if request.method == 'GET':
        return render_template('add_post.html')

    post_image = request.files.get('post_image')
    post_content = request.values.get('post_content')
    user_id = UserIDentifier().get_user_id(request)
    user_name = UserIDentifier().get_user_name(request)
    Repository().add_new_post(user_id, user_name, post_image, post_content)
    return redirect(url_for('main_blueprint.page_index'))
    pass

#actions
@main_blueprint.post('/post/<int:post_id>/leavecomment')
def comment_action(post_id):
    comment = request.values.get('comment_content')
    user_name = UserIDentifier().get_user_name(request)
    Repository().add_new_comment(post_id, user_name, comment)
    return redirect(url_for('main_blueprint.page_post', post_id=post_id), code=302)

@main_blueprint.post('/bookmark_action')
def bookmark_action():
    post_id = int(request.values.get('post_id'))
    user_id = UserIDentifier().get_user_id(request)

    Repository().set_bookmark_state(user_id, post_id)

    user_bookmarks = Repository().get_user_bookmarks(user_id)

    if post_id in user_bookmarks:
        return jsonify({'status': 'on'})
    else:
        return jsonify({'status': 'off'})

@main_blueprint.post('/like_action')
def like_action():
    post_id = int(request.values.get('post_id'))
    user_id = UserIDentifier().get_user_id(request)

    Repository().set_user_like_state(user_id, post_id)

    user_likes = Repository().get_user_likes(user_id)
    if post_id in user_likes:
        Repository().set_post_likes_counter(post_id, 1)
        return jsonify({'status': 'like'})
    else:
        Repository().set_post_likes_counter(post_id, -1)
        return jsonify({'status': 'dislike'})


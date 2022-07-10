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

    posts_by_search_line = Repository().get_post_by_search_line(search_line)


    return render_template('index.html', posts=posts_by_search_line, bookmarks=user_bookmarks, likes=user_likes, search=True)


#actions

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

    Repository().change_user_like_state(user_id, post_id)

    user_likes = Repository().get_user_likes(user_id)
    if post_id in user_likes:
        Repository().set_post_likes_counter(post_id, 1)
        return jsonify({'status': 'like'})
    else:
        Repository().set_post_likes_counter(post_id, -1)
        return jsonify({'status': 'dislike'})


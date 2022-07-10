import random

from flask import render_template, Blueprint, request, url_for, redirect
from project.globals import STATIC_PATH_ABS
from project.classes import UserIDentifier
from project.classes import Repository
# Включает в себя главную страницу, подробный пост

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='./templates', static_folder=STATIC_PATH_ABS)

@main_blueprint.get('/')
def page_index():
    if not UserIDentifier().is_user_registered(request):
        return redirect(url_for('reg_blueprint.page_reg'), code=302)

    all_posts = Repository().get_all_posts()
    return render_template('index.html', posts=all_posts)

@main_blueprint.post('/')
def get_like():
    test = random.choice(['like', 'dislike'])
    from flask import jsonify
    return jsonify({'status': test})


#
# @main_blueprint.route('/search')
# def search_page():
#     search_line = request.args['s']
#
#     try:
#         #грузим базу
#         db = DataBase(POSTS_FILE)
#     except BaseException as e:
#         return f'Ошибка: "{e}"'
#
#     #ищем соответствующие посты
#     search_result = db.search_str_in_db_data(search_line)
#
#     #возвращаем теплейт с постами
#     return render_template('searched_posts.html', search_line=search_line, posts=search_result)
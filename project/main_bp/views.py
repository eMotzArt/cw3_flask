from flask import render_template, Blueprint, request
from project.globals import STATIC_PATH_ABS
# Включает в себя главную страницу, подробный пост

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='./templates', static_folder=STATIC_PATH_ABS)


@main_blueprint.route('/')
def main_page():
    return render_template('index.html')

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
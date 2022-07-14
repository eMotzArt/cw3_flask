from flask import Blueprint, jsonify
from project.globals import STATIC_PATH_ABS
from project.classes import Repository

api_blueprint = Blueprint('api_blueprint', __name__, template_folder='./templates', static_folder=STATIC_PATH_ABS)

@api_blueprint.get('/api/posts')
def page_api_posts():
    all_posts = Repository().get_all_posts()
    return jsonify(all_posts)

@api_blueprint.get('/api/posts/<int:post_id>')
def page_api_post(post_id):
    post = Repository().get_post_by_id(post_id)
    return jsonify(post)

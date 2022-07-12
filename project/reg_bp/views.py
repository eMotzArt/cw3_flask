from flask import render_template, Blueprint, request, url_for, redirect
from project.globals import STATIC_PATH_ABS
from project.classes import UserIDentifier
from project.classes import Repository

reg_blueprint = Blueprint('reg_blueprint', __name__, template_folder='./templates', static_folder=STATIC_PATH_ABS)

@reg_blueprint.route('/reg/', methods=('GET', 'POST'))
def page_reg():
    if request.method == 'GET':
        return render_template('reg.html')

    if request.method == 'POST':
        UserIDentifier().register_new_user(request)
        return redirect(url_for('main_blueprint.page_index'))



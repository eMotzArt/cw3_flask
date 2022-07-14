from flask import Flask, send_from_directory, render_template
import os

from project.main_bp.views import main_blueprint
from project.reg_bp.views import reg_blueprint
from project.api_bp.views import api_blueprint

from project.globals import IMG_PATH_ABS, TEMPLATES_PATH_ABS


app = Flask(__name__, template_folder=TEMPLATES_PATH_ABS)

app.register_blueprint(main_blueprint)
app.register_blueprint(reg_blueprint)
app.register_blueprint(api_blueprint)

app.config['UPLOAD_FOLDER'] = IMG_PATH_ABS

#static route
@app.route("/static/<path:path>/<path:filename>")
def static_dir(path, filename):
    path_endpoint = os.path.join(path, filename)
    return send_from_directory("project/static", path_endpoint)


#error handler
@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error=e.name, error_code=e.code), e.code


if __name__ == '__main__':
    app.run()
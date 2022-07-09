from flask import Flask, send_from_directory

from project.main_bp.views import main_blueprint

app = Flask(__name__)

app.register_blueprint(main_blueprint)


@app.route("/static/<path:path>/<path:filename>")
def static_dir(path, filename):
    import os
    path_endpoint = os.path.join(path, filename)
    return send_from_directory("project/static", path_endpoint)


if __name__ == '__main__':
    app.run()
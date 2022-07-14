import pathlib

# абсолютные пути
ROOT_PATH_ABS = pathlib.Path(__file__).resolve().parent.parent
PROJECT_PATH_ABS = ROOT_PATH_ABS.joinpath('project')
TEMPLATES_PATH_ABS = ROOT_PATH_ABS.joinpath('project', 'templates')
STATIC_PATH_ABS = ROOT_PATH_ABS.joinpath('project', 'static')
IMG_PATH_ABS = ROOT_PATH_ABS.joinpath('project', 'static', 'img')
DATA_PATH_ABS = ROOT_PATH_ABS.joinpath('project', 'data')

# относительные пути
# ROOT_PATH = pathlib.PurePath(ROOT_PATH_ABS).relative_to(ROOT_PATH_ABS)
# PROJECT_PATH = pathlib.PurePath(PROJECT_PATH_ABS).relative_to(ROOT_PATH_ABS)
# DATA_PATH = pathlib.PurePath(DATA_PATH_ABS).relative_to(ROOT_PATH_ABS)
# TEMPLATES_PATH = pathlib.PurePath(TEMPLATES_PATH_ABS).relative_to(ROOT_PATH_ABS)
STATIC_PATH = pathlib.PurePath(STATIC_PATH_ABS).relative_to(ROOT_PATH_ABS)

pass
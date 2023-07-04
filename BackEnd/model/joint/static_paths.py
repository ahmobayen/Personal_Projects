from os import path

# Working Directories
BASE_PATH = path.abspath(path.dirname(path.dirname(path.dirname(__file__))))
STATIC_PATH = path.join(BASE_PATH, 'static/')
TRAINING_PATH = path.join(STATIC_PATH, 'training/')
VIDEO_PATH = path.join(STATIC_PATH, 'videos/')
LOGS_PATH = path.join(BASE_PATH, 'logs/')


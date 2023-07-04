<<<<<<< HEAD
# run.py

from app import create_app

config_name = 'development'
app = create_app(config_name)


if __name__ == '__main__':
=======
# run.py

from app import create_app

config_name = 'development'
app = create_app(config_name)


if __name__ == '__main__':
>>>>>>> 270786ff41f19b6230c41b27351db543564b1c60
    app.run()
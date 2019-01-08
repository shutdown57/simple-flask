import os


basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'you-will-never-guess'
DEBUG = True
BLOG_DATABASE_NAME = 'blog'
DB_URI = 'sqlite:///' + os.path.join(basedir, 'app.sqlite3')
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_IMAGES_DEST = basedir + '/static/images'
UPLOADED_IMAGES_URL = '/static/images/'

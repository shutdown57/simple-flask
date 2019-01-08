from flask_blog import db, uploaded_images
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('author.id'))
    posts = db.relationship('Post', backref='blog', lazy='dynamic')

    def __init__(self, name, admin):
        self.name = name
        self.admin = admin

    def __repr__():
        return '<Blog %r>' % self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    image = db.Column(db.String(255))
    slug = db.Column(db.String(256), unique=True)
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean) #used to hide posts rather than delete

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    comments = db.relationship('Comment', backref='posts', lazy='dynamic')

    @property
    def imgsrc(self):
        return uploaded_images.url(self.image)

    def __init__(self, blog, author, title, body, category, image=None, slug=None, publish_date=None, live=True):
        self.blog_id = blog.id
        self.author_id = author.id
        self.title = title
        self.body = body
        self.category_id = category.id
        self.image = image
        self.slug = slug
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date
        self.live = live

    def __repr__(self):
        return '<Post %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        #return '<Category %r>' % self.name
        return self.name

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    username = db.Column(db.String(50))
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    def __init__(self, author, post, body, publish_date=None, live=True):
        self.author_id = author.id
        self.username = author.username
        self.post_id = post.id
        self.body = body
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date
        self.live = live

    def __repr__(self):
        return '<Comment %r>' % self.body

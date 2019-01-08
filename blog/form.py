from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField
from author.form import RegisterForm
from blog.models import Category
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed

class SetupForm(RegisterForm):
    name = StringField('Blog name', [
        validators.Required(),
        validators.Length(max=80)
        ])

def categories():
    return Category.query

class PostForm(FlaskForm):
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
        ])
    title = StringField('Title', [
        validators.Required(),
        validators.Length(max=80)
        ])
    body = TextAreaField('Content', validators=[validators.Required()])
    category = QuerySelectField('Category', query_factory=categories, allow_blank=True)
    new_category = StringField('New Category')

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[validators.Required()])

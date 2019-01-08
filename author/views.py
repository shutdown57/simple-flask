from flask_blog import app, db
from flask import render_template, redirect, url_for, session, request, flash
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
from blog.models import Blog
import bcrypt

@app.route('/login', methods=('GET', 'POST'))
def login():
    blog = Blog.query.first()
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = Author.query.filter_by(
            username=form.username.data
            ).first()
        if author:
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                flash('User %s logged in' % form.username.data)
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
            else:
                error = "Incorrect username and password"
        else:
            error = "Incorrect username and password"
    return render_template('author/login.html', form=form, error=error, blog=blog)

@app.route('/register', methods=('GET', 'POST'))
def register():
    blog = Blog.query.first()
    form = RegisterForm()
    error = ""
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            False
            )
        db.session.add(author)
        db.session.flush()
        if author.id:
            db.session.commit()
            flash("User account created")
            return redirect(url_for('index'))
        else:
            db.session.rollback()
            error = "Error creating user"
    return render_template('author/register.html', form=form, error=error, blog=blog)

@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('is_author')
    flash("User logged out")
    return redirect(url_for('index'))

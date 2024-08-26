from sqlalchemy.sql import func

from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from flask_babel import _, get_locale
from flask import g

from app import app, db
from app.email import send_password_reset_email
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, \
    ResetPasswordForm
from app.models import User, Post


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = func.now()
        db.session.commit()

    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'), 'info')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html', title='Home', form=form, posts=posts, next_url=next_url, prev_url=prev_url)


@app.route("/explore")
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = (Post
             .query
             .order_by(Post.timestamp.desc())
             .paginate(page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False))
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('explore.html', title='Explore', posts=posts, next_url=next_url, prev_url=prev_url)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'), 'error')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'), 'warning')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    print(username)
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template("user.html", user=user, posts=posts, next_url=next_url, prev_url=prev_url)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'), 'info')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash(_('User %(username)s not found.', username=username), 'error')
        return redirect(url_for('index'))

    if user == current_user:
        flash(_('You cannot follow yourself!'), 'error')
        return redirect(url_for('user', username=username))

    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username), 'info')
    return redirect(url_for('user', username=username))


@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash(_('User %(username)s not found.', username=username), 'error')
        return redirect(url_for('index'))

    if user == current_user:
        flash(_('You cannot unfollow yourself!'), 'error')
        return redirect(url_for('user', username=username))

    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s!', username=username), 'info')
    return redirect(url_for('user', username=username))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            send_password_reset_email(user)

        flash(_('Check your email for the instructions to reset your password.'), 'info')
        return redirect(url_for('login'))

    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        redirect(url_for('index'))

    user = User.verify_reset_password_token(token)

    if user is None:
        return redirect(url_for('index'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'), 'info')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


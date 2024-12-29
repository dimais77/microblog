from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from datetime import datetime, timezone


@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'Дмитрий'}
    posts = [
        {
            'author': {'username': 'Валентина'},
              'body': '"Синица" - небольшая уютная студия, в которой мы постарались создать условия '
                      'для того, чтобы каждый ребёнок мог проявить себя в области художественного '
                      'творчества. Мы предоставим всё необходимое для занятий (бумагу, кисти, '
                      'краски, карандаши и прочее). Мы будем рисовать, делать аппликации, коллажи,'
                      'оттиски, барельефы и ещё много всего! Наша цель - вдохновить на творчество! '
                      'Показать, что рисовать легко, весело и интересно!'
        },
        {'author': {'username': 'Инна'},
         'body': 'Дочь занимается в этой студии рисованием и пластилинографией. Очень нравится! '
                 'Помещение очень уютное, удобно припарковаться, педагог Валентина профессиональна '
                 'и находит индивидуальный подход к каждому ребенку.'
         },
        {
            'author': {'username': 'Татьяна'},
            'body': 'Уютное, камерное пространство, в котором хочется заниматься творчеством. '
                    'Очень ждём, когда будет группа для взрослых.'
        }
    ]
    return render_template('index.html', title='Главная', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, Вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Редактировать профиль', form=form)

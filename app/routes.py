from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Дмитрий'}
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
    return render_template('index.html', title='Главная', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Авторизация', form=form)

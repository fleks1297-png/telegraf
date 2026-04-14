import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from forms import ArticleForm, LoginForm, RegisterForm
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'blog.db')
app.config['SECRET_KEY'] = 'your-secret-key-here'
db = SQLAlchemy(app)

# Декоратор для редиректа на логин
def login_required_redirect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    articles = db.relationship('Article', backref='author', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
@login_required_redirect
def index():
    page = request.args.get('page', 1, type=int)
    posts = Article.query.order_by(Article.date.desc()).paginate(page=page, per_page=5, error_out=False)
    return render_template('index.html', posts=posts)

@app.route('/post/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    if article is None:
        return "Статья не найдена", 404
    return render_template('post_detail.html', article=article)

@app.route('/article/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_article(id):
    article = Article.query.get_or_404(id)
    
    if article.author_id != current_user.id:
        abort(403)
        
    form = ArticleForm()
    
    if form.validate_on_submit():
        article.title = form.title.data
        article.intro = form.intro.data
        article.text = form.text.data
        
        try:
            db.session.commit()
            flash('Статья успешно обновлена', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'При обновлении статьи произошла ошибка: {str(e)}', 'danger')
            
    elif request.method == 'GET':
        form.title.data = article.title
        form.intro.data = article.intro
        form.text.data = article.text
        
    return render_template('create_article.html', form=form, is_update=True)

@app.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def post_update(id):
    article = Article.query.get(id)
    if article is None:
        return "Статья не найдена", 404
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.intro = form.intro.data
        article.text = form.text.data
        db.session.commit()
        flash('Статья обновлена!', 'success')
        return redirect(url_for('post_detail', id=id))
    form.title.data = article.title
    form.intro.data = article.intro
    form.text.data = article.text
    return render_template('create_article.html', form=form)

@app.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def post_delete(id):
    article = Article.query.get_or_404(id)
    
    if article.author_id != current_user.id:
        abort(403)
        
    try:
        db.session.delete(article)
        db.session.commit()
        flash('Статья была успешно удалена.', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Ошибка при удалении: {str(e)}', 'danger')
        return redirect(url_for('post_detail', id=id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email уже занят', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Обработчик ошибки 404 (Страница не найдена)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Обработчик ошибки 403 (Доступ запрещен)
@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True, port=9090)

@app.route('/render/contacts')
def render_contacts():
    return render_template('contacts_content.html')

@app.route('/render/chats')
def render_chats():
    return render_template('chats_content.html')

@app.route('/render/settings')
def render_settings():
    return render_template('settings_content.html')

from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configuration
ARTICLES_DIR = 'articles'
os.makedirs(ARTICLES_DIR, exist_ok=True)

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = generate_password_hash('admin123')

# Helper functions (same as before)
def get_article_filename(article_id):
    return os.path.join(ARTICLES_DIR, f'{article_id}.json')

def get_all_articles():
    articles = []
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(ARTICLES_DIR, filename), 'r') as f:
                article = json.load(f)
                article['id'] = filename[:-5]
                articles.append(article)
    return sorted(articles, key=lambda x: x['date'], reverse=True)

def save_article(article_id, title, content, date):
    article = {'title': title, 'content': content, 'date': date}
    with open(get_article_filename(article_id), 'w') as f:
        json.dump(article, f)

def delete_article(article_id):
    try:
        os.remove(get_article_filename(article_id))
    except FileNotFoundError:
        pass

# Authentication decorator
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__  # This prevents the endpoint conflict
    return decorated_function

# Routes
@app.route('/')
def home():
    articles = get_all_articles()
    return render_template('guest/home.html', articles=articles)

@app.route('/article/<article_id>')
def article(article_id):
    try:
        with open(get_article_filename(article_id), 'r') as f:
            article = json.load(f)
        return render_template('guest/article.html', article=article)
    except FileNotFoundError:
        abort(404)

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('auth/login.html')

@app.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    articles = get_all_articles()
    return render_template('admin/dashboard.html', articles=articles)

@app.route('/admin/new', methods=['GET', 'POST'])
@admin_required
def new_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        date = request.form.get('date') or datetime.now().strftime('%Y-%m-%d')
        if not title or not content:
            flash('Title and content are required', 'error')
        else:
            article_id = str(int(datetime.now().timestamp()))
            save_article(article_id, title, content, date)
            flash('Article published successfully', 'success')
            return redirect(url_for('admin_dashboard'))
    return render_template('admin/new.html')

@app.route('/admin/edit/<article_id>', methods=['GET', 'POST'])
@admin_required
def edit_article(article_id):
    try:
        with open(get_article_filename(article_id), 'r') as f:
            article = json.load(f)
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            date = request.form.get('date')
            if not title or not content:
                flash('Title and content are required', 'error')
            else:
                save_article(article_id, title, content, date)
                flash('Article updated successfully', 'success')
                return redirect(url_for('admin_dashboard'))
        return render_template('admin/edit.html', article=article, article_id=article_id)
    except FileNotFoundError:
        abort(404)

@app.route('/admin/delete/<article_id>')
@admin_required
def delete_article_route(article_id):
    delete_article(article_id)
    flash('Article deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.context_processor
def inject_now():
    return {'now': datetime.now()}
if __name__ == '__main__':
    app.run(debug=True)
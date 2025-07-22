import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from ..database import add_url, get_url_by_id, get_all_urls

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        url = request.form.get('url')
        url_id, error = add_url(url)
        if error:
            flash(error, 'danger')
            return render_template('index.html'), 422
        flash('Страница успешно добавлена', 'seccess')
        return redirect(url_for('url_detail', id=url_id))

    urls = get_all_urls()
    return render_template('urls.html', urls=urls)

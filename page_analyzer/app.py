import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from page_analyzer import database, checker, validator

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        url_input = request.form.get('url')
        if not validator.is_valid_url(url_input):
            error = 'Некорректный URL' if url_input else 'Заполните это поле.'
            flash(error, 'danger')
            return render_template('index.html'), 422
        parsed_url = validator.normalize_url(url_input)
        url_id, error = database.add_url(parsed_url)
        if error:
            flash(error, 'danger')
            return render_template('index.html'), 422
        flash('Страница успешно добавлена', 'seccess')
        return redirect(url_for('url_detail', id=url_id))

    urls = database.get_all_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>', methods=['GET', 'POST'])
def url_detail(id):
    url = database.get_url_by_id(id)
    if not url:
        flash('URL не найден', 'danger')
        return redirect(url_for('urls'))
    if request.method == 'POST':
        try:
            status_code, h1, title, description = checker.check_url(url[1])
            database.add_check(id, status_code, h1, title, description)
            flash('Страница успешно проверена', 'success')
        except checker.CheckError:
            flash('Ошибка проверки: не удалось подключиться к сайту', 'danger')
        return redirect(url_for('url_detail', id=id))
    return render_template('url_detail.html', url=url)

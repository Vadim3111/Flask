from flask import Flask, render_template, request,redirect, url_for, session

app = Flask(__name__)

app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/', methods=['GET', 'POST'])
def login():
    context = {
        'login': 'Авторизация'
    }
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['email'] = request.form.get('email')
        return redirect(url_for('success'))
    return render_template('login.html', **context)


@app.route('/success/', methods=['GET', 'POST'])
def success():
    if 'name' in session:
        context = {
            'name': session['name'],
            'email': session['email'],
            'title': 'Добро пожаловать'
        }
        if request.method == 'POST':
            session.pop('name', None)
            session.pop('email', None)
            return redirect(url_for('login'))
        return render_template('success.html', **context)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
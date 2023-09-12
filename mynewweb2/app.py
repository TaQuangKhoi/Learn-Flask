from flask import Flask, url_for, request
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/mylove')
def my_love():
    return 'My love is nobody'


@app.route('/mylove/<name>')
def who_is_my_love(name):
    if name == 'me':
        return 'My love is myself'
    return f'My love is {escape(name)}'


def do_the_login():
    return 'Login'


def show_the_login_form():
    return 'Login form'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


@app.get('/signup')
def signup_get():
    return show_the_login_form()


@app.post('/signup')
def signup_post():
    return do_the_login()


with app.test_request_context():
    print(url_for('my_love'))
    print(url_for('my_love', next='/'))
    print(url_for('who_is_my_love', name='Hảo Văn'))

if __name__ == '__main__':
    app.run()
from flask import Flask
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


if __name__ == '__main__':
    app.run()

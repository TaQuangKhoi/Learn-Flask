from flask import Flask, url_for
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


with app.test_request_context():
    print(url_for('my_love'))
    print(url_for('my_love', next='/'))
    print(url_for('who_is_my_love', name='Hảo Văn'))

if __name__ == '__main__':
    app.run()

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/mylove/<name>')
def who_is_my_love(name):
    return 'My love is ' + name


if __name__ == '__main__':
    app.run()

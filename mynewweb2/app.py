from flask import Flask, url_for, request, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/mylove/')
@app.route('/mylove/<name>')
def who_is_my_love(name=None):
    return render_template('Hảo Văn.html', name=name)


def do_the_login():
    return render_template('login.html')


def show_the_login_form():
    return render_template('login.html')


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
    print(url_for('who_is_my_love', name='Hảo Văn'))
    print(url_for('static', filename='style.css'))

if __name__ == '__main__':
    app.run()

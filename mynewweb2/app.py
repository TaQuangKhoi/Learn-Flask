from flask import Flask, url_for, request, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


def do_the_login(req):
    # data from form
    # username = req.form['username']
    # print(username)
    # password = req.form['password']
    # print(password)
    return 'Done'


def show_the_login_form():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # List of all data in request
        print(request.values.keys())

        return do_the_login(request)
    else:
        return show_the_login_form()


@app.get('/signup')
def signup_get():
    return show_the_login_form()


@app.post('/signup')
def signup_post():
    return do_the_login()


with app.test_request_context():
    print(url_for('static', filename='style.css'))

if __name__ == '__main__':
    app.run()

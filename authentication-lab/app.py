from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
"apiKey": "AIzaSyApZzDZSlsP57ae-epXKyWxf9K_WxA5FZI",
"authDomain": "first-e71e8.firebaseapp.com",
"projectId": "first-e71e8",
"storageBucket": "first-e71e8.appspot.com",
"messagingSenderId": "187746478309",
"appId": "1:187746478309:web:2e462a6e5370414c8a4c0c",
"measurementId": "G-K68685HPFJ",
"databaseURL": ""
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
			return render_template("signin.html")
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
			return render_template("signup.html")
	return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyDaDeRHWUnD59hgaD9ZNDtZg49y-RMtKWk",
  "authDomain": "first-firebase-ff06e.firebaseapp.com",
  "projectId": "first-firebase-ff06e",
  "storageBucket": "first-firebase-ff06e.appspot.com",
  "messagingSenderId": "1053387551914",
  "appId": "1:1053387551914:web:4276f2616109aea6b08cd3",
  "measurementId": "G-6BZJYTVZTR",
  "databaseURL": "https://first-firebase-ff06e-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
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
            user = {"name": request.form['name'], "email":request.form['email'], "bio": request.form["bio"], "username": request.form["username"], "password": request.form["password"]}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
            
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        title = request.form["title"]
        text = request.form["text"]
        uid = db.child("Users").child(login_session['user']['localId']).get().val()
        
        #try:
        tweet = {"title": title, "text": text, "uid": uid}
        db.child("Tweets").push(tweet)
        

        return redirect(url_for('all_tweets'))
        #except:
        print("Couldn't add tweet")
        return render_template("add_tweet.html")
    return render_template("add_tweet.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))
    
@app.route('/all_tweets', methods = ['GET', 'POST'])
def all_tweets():
    tweet = db.child("Tweets").get().val()


    return render_template("all_tweets.html", t = tweet)
if __name__ == '__main__':
    app.run(debug=True)
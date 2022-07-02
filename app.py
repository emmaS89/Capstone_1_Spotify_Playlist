import os

import datetime
import random
from flask_wtf import csrf
from flask import request, Flask, render_template, jsonify, redirect, session , flash
from spotipy.oauth2 import SpotifyClientCredentials
import random
import spotipy
import spotipy.util as util

import spotipy
from models import db ,connect_db, User , PlayedSong
from forms import LoginForm , Signupform
from datetime import timedelta
from flask_debugtoolbar import DebugToolbarExtension

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

import credentials

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///spot'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://dqcoegzqmhmthe:2b4b9bd3daf925adc8bf61d470d7c57af004bee6aa08cf53838c9855796dd245@ec2-3-222-74-92.compute-1.amazonaws.com:5432/ddonek0fq9rjqr'

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "heysecret!!122") 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


connect_db(app)
db.create_all()



login_manager.init_app(app)
# debug = DebugToolbarExtension(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


def getAllSongsDataFromSpotify():
    final_list = []
    client_credentials_manager = SpotifyClientCredentials(client_id=credentials.client_id,
                                                          client_secret= credentials.client_secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    data = sp.user_playlists('spotify')

    Playlists = []
    for item in data['items']:
        Playlists.append(item['id'])

    playLists = Playlists
    count = 1

    for l in random.sample(playLists , 4):
        data = sp.playlist_tracks(playlist_id=l)['items']
        cat_song = []
        for row in data:
            try:
                cat_song.append({'name': row['track']['name'],
                             'artistname': row['track']['artists'][0]['name'],
                             'images': row['track']['album']['images']})
            except:
                pass

        final_list.append({'categoryName': f'category {count}', 'data': cat_song})
        count += 1
    print(len(final_list))
    return final_list


@app.route("/")
def homepage():
    """Show homepage."""
    if current_user.is_authenticated:
        data = getAllSongsDataFromSpotify()

        return render_template("index.html", songs=data , user=current_user)
    else:
        return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def login():
    """Show login page."""
    loginForm = LoginForm()

    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        loginForm.email.data = request.form.get('email')
        loginForm.password.data = request.form.get('password')

        user = User.query.filter_by(email=loginForm.email.data).first()

        if user and user.password == loginForm.password.data:
            user.authenticated  =True
            user.is_active = True

            login_user(user)
        else:
            flash('Email or password is incorrect' , "danger")

            return render_template("login.html", error="Email or password is wrong")
        flash('Login success', "success")

        return redirect('/')

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Show signup page."""
    signup_form = Signupform()

    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        signup_form.username.data = request.form.get('username')
        signup_form.email.data = request.form.get('email')
        signup_form.password.data = request.form.get('password')
        signup_form.confirmPassword.data = request.form.get('confirm-password')

        data = User.query.filter_by(email=signup_form.email.data).first()
        if data:
            flash('Email already registered in data kindly provide anther email', "danger")
            return render_template("signup.html", msg="Email already registered!")

        user = User()
        user.name = signup_form.username.data
        user.password = signup_form.password.data
        user.email = signup_form.email.data

        db.session.add(user)
        db.session.commit()
        flash('Signup Success Kindly Login', "success")

        return redirect('/login')

    return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    """Show homepage."""

    logout_user()
    flash('Logout success', "success")

    return redirect('/login')


@app.route("/playlists")
def playlists():
    if current_user.is_authenticated:
        data = PlayedSong.query.filter_by(user_id=current_user.id).all()
        return render_template('playlist.html', data=data , user=current_user , count=len(data))
    else:
        return redirect('/login')


@app.route("/addToPlayList", methods=["GET", "POST"])
def addToPlayList():
    play_song = PlayedSong()

    if current_user.is_authenticated:
        play_song.song_name = request.form.get('name')
        play_song.url = request.form.get('url')
        play_song.time = "4:30"
        play_song.addedAt = str(datetime.date.today())
        play_song.user_id = current_user.id

        db.session.add(play_song)
        db.session.commit()
        flash('song added to Playlist successfully', "success")

        return redirect('/playlists')
    else:
        return redirect('/login')

@app.route("/playlists/<int:playlist_id>/delete")
def deleteById(playlist_id):
    if current_user.is_authenticated:
        data = PlayedSong.query.filter_by(id=playlist_id).one()

        db.session.delete(data)
        db.session.commit()
        flash('song remove from Playlist successfully', "success")

        return redirect("/playlists")
    else:
        return redirect('/login')
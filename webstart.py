#!/usr/bin/env python3
from flask import Flask, render_template, request, session, abort, g, redirect, url_for
import sqlite3
import os
import db
import settings
from functools import wraps

GAMEMODETEXT = "gamemodetext.txt"

# This sets up flask to work properly
 
app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		leaderboard = []
		with db.getCur() as cur:
			cur.execute("SELECT Username, ViewCount, LastView FROM Viewers ORDER BY ViewCount DESC LIMIT ?", (settings.LEADERLENGTH,))
			leaderboard = cur.fetchall()
			cur.execute("SELECT Username FROM CurrentViewers")
			currentviewers = [viewer[0] for viewer in cur.fetchall()]
			if os.path.isfile(GAMEMODETEXT):
				gamemode = open(GAMEMODETEXT).read()
			else: 
				gamemode = ""
		return render_template('dashboard.html',leaderboard=leaderboard, TWITCH_CHANNEL=settings.TWITCH_CHANNEL, currentviewers=currentviewers, gamemode=gamemode)

@app.route('/obs')
def obs():
	if os.path.isfile(GAMEMODETEXT):
		gamemode = open(GAMEMODETEXT).read()
	else: 
		gamemode = ""
	return render_template('obs.html', gamemode=gamemode)

@app.route('/', methods=["POST"])
def do_admin_login():
	if request.form['password'] == settings.PASSWORD and request.form['username'].lower() == settings.USER_ACCOUNT.lower():
		session['logged_in'] = True
	return home()

@app.route('/Dashboard', methods=["POST"])
def storeGamemode():
	with open(GAMEMODETEXT, 'w+') as tmp:
		tmp.write(str(request.form["gametype"]))
	return redirect('/')

app.secret_key = settings.SECRETKEY

if __name__=='__main__':
	db.createTables()
	app.run(host='0.0.0.0', port=80)



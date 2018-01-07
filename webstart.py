#!/usr/bin/env python3
from flask import Flask, render_template, request, session, abort, g, redirect, url_for
import sqlite3
import os
import db
import settings
from functools import wraps
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
		return render_template('dashboard.html',leaderboard=leaderboard, TWITCHCHANNEL=settings.TWITCHCHANNEL, currentviewers=currentviewers)

@app.route('/', methods=["POST"])
def do_admin_login():
	if request.form['password'] == settings.PASSWORD and request.form['username'].lower() == settings.USERACCOUNT.lower():
		session['logged_in'] = True
	return home()

app.secret_key = settings.SECRETKEY

if __name__=='__main__':
	db.createTables()
	app.run(host='0.0.0.0', port=8000)



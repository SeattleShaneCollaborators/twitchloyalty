#!/usr/bin/env python3
from flask import Flask, render_template
import sqlite3

import db
import settings

# This sets up flask to work properly
app = Flask(__name__)
@app.route("/")
def getLeaderboard():
	leaderboard = []
	with db.getCur() as cur:
		cur.execute("SELECT Username, ViewCount, LastView FROM Viewers ORDER BY ViewCount DESC LIMIT ?", (settings.LEADERLENGTH,))
		leaderboard = cur.fetchall()
	return render_template('index.html',leaderboard=leaderboard, TWITCHCHANNEL=settings.TWITCHCHANNEL)

if __name__=='__main__':
	db.createTables()
	app.run(host='0.0.0.0', port=8000)

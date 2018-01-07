#!/usr/bin/env python3
import requests
import json
import sqlite3
from datetime import datetime
import settings
import db


def updateCurrentViewers(viewers):
        with db.getCur() as cur:
                cur.executemany("INSERT OR IGNORE INTO CurrentViewers VALUES(?);",list(zip(viewers)))
        with open(settings.LOG, 'a') as logfile:
                logfile.write(str(datetime.now()) + "   Updated CurrentViewers" + '\n')

def clearCurrentViewers():
        with db.getCur() as cur:
                cur.execute("DELETE FROM CurrentViewers;")

def incrementViewer(viewer):
        with db.getCur() as cur:
                    cur.execute("INSERT OR REPLACE INTO Viewers VALUES (?,COALESCE((SELECT ViewCount + 1 FROM Viewers WHERE Username = ?), 1),DATETIME('now'));",(viewer,viewer))
        with open(settings.LOG, 'a') as logfile:
                logfile.write(str(datetime.now()) + "   Incremeted Viewers" + '\n')


def updateViewerTimes(viewers):
        with db.getCur() as cur:
                    cur.executemany("UPDATE Viewers SET Lastview = DATETIME('now') WHERE Username = ?;",list(zip(viewers)))

def isChannelLive():
	print('Beginning file download live status from twitch' + settings.TWITCHCHANNEL)
	url = 'https://api.twitch.tv/helix/streams?user_login=' + settings.TWITCHCHANNEL
	header = {'Client-ID': settings.CLIENT_ID}
	r = requests.get(url, headers=header)
	tmp = json.loads(r.content.decode('utf-8'))
	if len(tmp['data']) != 0:
		return tmp['data'][0]['type'] == "live"
	else: 
		return False

#Returns the list of viewers from the current session
def getCurrentViewers():
        with db.getCur() as cur:
                cur.execute("SELECT * FROM CurrentViewers")
                return [viewer[0] for viewer in cur.fetchall()]

def getChatters():
        print('Beginning file download from tmi.twitch.tv/' + settings.TWITCHCHANNEL)
        url ='https://tmi.twitch.tv/group/user/' + settings.TWITCHCHANNEL + '/chatters'
        try:
                r = requests.get(url)
                tmp = json.loads(r.content.decode('utf-8'))
                return tmp["chatters"]
        except (ValueError, TypeError, KeyError):
                raise RuntimeError('Could not get twitch JSON, check TWITCHANNEL')

def getViewers(chatters):
        return chatters["viewers"]

def isLive(chatters):
        return settings.TWITCHCHANNEL in chatters["moderators"]

# This goes through the CURRENT viewers and compares them against the table of viewers
def incrementViewers():
        chatters = getChatters()
        viewers = getViewers(chatters)
        if isChannelLive():
            currentViewers = getCurrentViewers()
            for viewer in viewers:
                    if viewer not in currentViewers:
                            incrementViewer(viewer)
            updateViewerTimes(viewers)
            updateCurrentViewers(viewers)
        else:
            clearCurrentViewers()

if __name__ == "__main__":
        db.createTables()
        incrementViewers()

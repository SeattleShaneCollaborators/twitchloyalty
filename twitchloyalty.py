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
                    cur.execute("INSERT OR REPLACE INTO Viewers VALUES (?,COALESCE((SELECT ViewCount + 1 FROM Viewers WHERE Username = ?), 1),DATETIME('now'$
        with open(settings.LOG, 'a') as logfile:
                logfile.write(str(datetime.now()) + "   Incremeted Viewers" + '\n')


def updateViewerTimes(viewers):
        with db.getCur() as cur:
                    cur.executemany("UPDATE Viewers SET Lastview = DATETIME('now') WHERE Username = ?;",list(zip(viewers)))

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
        except (ValueError, TypeError):
                raise StandardError('Could not get twitch JSON, check TWITCHANNEL')

def getViewers(chatters):
        return chatters["viewers"]

def isLive(chatters):
        return settings.TWITCHCHANNEL in chatters["moderators"]

# This goes through the CURRENT viewers and compares them against the table of viewers
def incrementViewers():
        chatters = getChatters()
        viewers = getViewers(chatters)
        if isLive(chatters):
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

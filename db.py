import sqlite3
import settings

# This sets up the SQLite and creates a cursor which creates, edits and stores values
class getCur():
	con = None
	cur = None
	def __enter__(self):
		self.con = sqlite3.connect(settings.DBFILE)
		self.cur = self.con.cursor()
		self.cur.execute("PRAGMA foreign_keys = 1;")
		return self.cur
	def __exit__(self, type, value, traceback):
		if self.cur and self.con and not value:
			self.cur.close()
			self.con.commit()
			self.con.close()
		return False

#This creates the SQLite Table
def createTables():
	with getCur() as cur:
		cur.execute("CREATE TABLE IF NOT EXISTS CurrentViewers(Username TEXT PRIMARY KEY);")
		cur.execute("CREATE TABLE IF NOT EXISTS Viewers(Username TEXT PRIMARY KEY, ViewCount INTEGER, Lastview DATETIME);")

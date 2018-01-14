# twitchloyalty
To do:

Get Twitch Authorized for callistergamingtv
https://dev.twitch.tv/docs/authentication

Use the AUTH token to get the stream ID and be albe to pull requsts from the twitch API.


https://dev.twitch.tv/docs/api/reference
 
 Once Entered use https://api.twitch.tv/helix/streams?user_id="CallistergamingTV" and get the ID
 
 WIth the ID then proceed to setup the trigger to increment viewers
 
 Example: This is wrong but general idea
 
 def getLive():
	print('Checking to see if session is active')
	url ='https://api.twitch.tv/helix/streams?' + settings.USERID
	r = requests.get(url)
	try:
		tmp = json.loads(r.content.decode('ascii'))
	return tmp["data"]["type"]
	except ValueError:
		print('Cannot get session state, check AUTH token or USERID')
  
 def isLive():
  if getLive == "live":
    return True
  else:
    return False
 
 def incrementViewer(viewer):
 while isLive == True:
  with getCur() as cur:
		cur.execute("SELECT EXISTS(SELECT * FROM Viewers  WHERE Username = ?)",(viewer,))
		if cur.fetchone()[0] == 0:
  			cur.execute("INSERT INTO Viewers VALUES (?,1,DATETIME('now'));",(viewer,))
			cur.execute("UPDATE Viewers SET Lastview = DATETIME('now') WHERE Username = ?;",(viewer,))
		else:
			cur.execute("UPDATE Viewers SET ViewCount = ViewCount + 1 WHERE Username = ?;",(viewer,))
      
 if __name__ == "__main__":
	createTables()
	incrementViewers()

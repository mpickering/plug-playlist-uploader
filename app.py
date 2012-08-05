import requests,time
import gdata.youtube
import gdata.youtube.service
import json, os
from flask import Flask,render_template, request,redirect, escape, session


app = Flask(__name__)

@app.route('/')
def index():
	def GetAuthSubUrl():
  		next = 'http://plug2youtube.herokuapp.com/auth'
  		scope = 'http://gdata.youtube.com'
  		secure = False
  		session = True
		yt_service = gdata.youtube.service.YouTubeService()
		return yt_service.GenerateAuthSubURL(next, scope, secure, session)
	if 'yt_service' in session:
		user_id=session['yt_service'].GetYouTubeUserEntry(username='default')
	return render_template('authed.html', name=None if not 'yt_service' in session else user_id.username.text, authed='yt_service' in session, youtubeLink = None if 'yt_service' in session else GetAuthSubUrl() )

@app.route('/auth', methods=['GET'])
def auth():
	if 'yt_service' not in session:
		token=request.args.get('token','')
		session['yt_service'] = gdata.youtube.service.YouTubeService()
		session['yt_service'].developer_key = os.environ['YOUTUBE_KEY']
		session['yt_service'].client_id = 'playlist-uploader'
		session['yt_service'].SetAuthSubToken(token)
		session['yt_service'].UpgradeToSessionToken()
	return redirect('/')
	

@app.route('/upload', methods=['POST'])
def upload():
	name = request.form['name']
	try:
		new_playlist = session['yt_service'].AddPlaylist(name, '')
	except:
		return json.dumps({'error': 'Playlist already exists'})
	else:
		session['playlist_uri'] = str(new_playlist.feed_link[0].href)
	return str(new_playlist.GetAlternateLink().href)

@app.route('/track', methods=['POST'])
def tracks():
	try:
		playlist_video_entry = session['yt_service'].AddPlaylistVideoEntryToPlaylist(session['playlist_uri'], request.form['id'])
	except:
		return json.dumps({'id':request.form['id'], 'state': 'missing' })
	return json.dumps({'id':request.form['id'], 'state': 'success' })


@app.route('/logout')
def logout():
	if 'yt_service' in session:
		session.pop('yt_service', None)
	return redirect('/')


@app.route('/progress')
def progress():
	if 'counts' in session:
		return json.dumps(session['counts'])

app.secret_key = os.environ['SECRET_KEY']

if __name__ == '__main__':
	    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
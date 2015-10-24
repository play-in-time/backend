from flask import Flask, request, json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'This is a!'

@app.route('/tracks_for_duration')
def tracks_for_duration():
	#return flask.jason.jsonify()
	pass

@app.route('/update_tracklist')
def update_tracklist():
	pass

@app.route('just_play')
def just_play():
	pass



if __name__ == '__main__':
    app.run(debug=True)
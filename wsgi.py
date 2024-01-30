from project import create_app
# from .extensions import socketio

app = create_app(testing=True)

if __name__ == "__main__":
	# socketio.run(app)
	app.run(debug=False, host='127.0.0.1', port=9898, use_reloader=False)
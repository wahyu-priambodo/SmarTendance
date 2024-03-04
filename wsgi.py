from project import create_app
# from .extensions import socketio

app = create_app(testing=True)

if __name__ == "__main__":
	# socketio.run(app)
	app.run()

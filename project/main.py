from . import create_app
from .extensions import socketio

if __name__ == "__main__":
	app = create_app(testing=True)
	socketio.run(app)

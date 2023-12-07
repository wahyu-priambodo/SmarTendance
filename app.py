from flask import Flask, render_template, make_response, jsonify, request

# instance a flask object as the flask app
app = Flask(__name__)

# create a simple route with the method index
@app.route('/')
def index():
	return '<h1>Hello from Flask app</h1>'

if __name__ == "__main__":
	app.run(debug=True) # run the flask app
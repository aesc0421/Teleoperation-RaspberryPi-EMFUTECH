from flask import Flask 
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route("/")
def ping():
    return "",200

def run_flask_server():
    print("Starting flask server")
    app.run(host="0.0.0.0", port=3000)
# main.py

from flask import Flask
from app.routes import register_routes

app = Flask(__name__)



if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask
from flask_cors import CORS
from src.app.mvt import mvt
from src.app.api import api

app = Flask(__name__, static_folder='./templates/images')
CORS(app)

app.register_blueprint(api)
app.register_blueprint(mvt)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask
from flask_cors import CORS
from controllers.test_controller import test_blueprint
from controllers.flash_card_controller import flash_card_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(test_blueprint)
app.register_blueprint(flash_card_blueprint)


@app.route('/')
def home():
    return '<h1>Hello world</h1>'



if __name__ == '__main__':
    # app.run(hos, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
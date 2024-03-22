from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SAIJFSDAKJFHFAGFFKSDJFANIGER1QK31'
    
    return app
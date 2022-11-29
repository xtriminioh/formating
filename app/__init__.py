import os

from dotenv import load_dotenv

from flask import Flask, redirect, url_for

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path,'app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #registro  init-db commmand
    from . import db
    db.init_app(app)

    #registro del blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    #routes
    @app.route('/')
    def home():
        return redirect(url_for("auth.login"))

    return app

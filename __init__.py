"""Initialize app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from Permansys import pms, ISO, risk, jobdesc, Post, Training, Competency, keykpi, Strategy, Contract
from Permansys.pmsdb import dbpms
from flaspms import testFlask
from flaspms.testFlask import dbs
from flaspms.models import dbsuk
import pymysql


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    #app.config.from_object('config.Config')
    #app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root22011963@localhost:3308/suk"
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://dev_apps:dev_apps!@#@192.168.196.100:3306/pms"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root22011963@localhost:3308/pms"
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///suku2.db3"
    app.config['ED_FOLDER'] = "C:/UED"
    app.secret_key = os.urandom(24)
    # app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=9)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DB_SERVER'] = 'localhost'
    app.config['UPLOAD_FOLDER'] = "C:/upload"
    app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 100

    # Initialize Plugins
    db.init_app(app)
    dbpms.init_app(app)
    dbsuk.init_app(app)
    dbs.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Import parts of our application

        # Register Blueprints
        app.register_blueprint(testFlask.app_tf)
        app.register_blueprint(pms.pms_bp, url_prefix='/pms')
        app.register_blueprint(ISO.iso, url_prefix='/iso')
        app.register_blueprint(risk.risk, url_prefix='/risk')
        app.register_blueprint(jobdesc.job, url_prefix='/job')
        app.register_blueprint(Post.post, url_prefix='/post')
        app.register_blueprint(Training.trn, url_prefix='/trn')
        app.register_blueprint(Competency.comt, url_prefix='/comt')
        app.register_blueprint(keykpi.kpi, url_prefix='/kpi')
        app.register_blueprint(Strategy.Strategy, url_prefix='/Strategy')
        app.register_blueprint(Contract.contract, url_prefix='/contract')

        return app

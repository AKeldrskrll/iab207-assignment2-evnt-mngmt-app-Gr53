# import flask - from 'package' import 'Class'
import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import date, timedelta
from decimal import Decimal
from threading import Lock
from flask_bcrypt import generate_password_hash

db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    # Should be set to false in a production environment
    app.debug = True
    app.secret_key = 'somesecretkey'

    instance_dir = os.path.join(app.root_path, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    db_path = os.path.join(instance_dir, 'sitedata.sqlite')
    # set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path.replace('\\', '/')
    # initialise db with flask app
    db.init_app(app)
    Bootstrap5(app)
    
    # initialise the login manager
    login_manager = LoginManager()
    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    # Importing inside the create_app function avoids circular references
    @login_manager.user_loader
    def load_user(user_id):
       from .models import User
       return db.session.scalar(db.select(User).where(User.id == user_id))

    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    # error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500
    
    app.config.setdefault("INIT_DONE", False)
    _init_lock = Lock()

    def _ensure_seeded_once():
        
        with _init_lock:
            if app.config["INIT_DONE"]:
                return
            from .models import User, Event
            db.create_all()

            any_event = db.session.scalar(db.select(Event).limit(1))
            if not any_event:
                # seed demo user
                demo = db.session.scalar(db.select(User).where(User.email == "demo@example.com"))
                if not demo:
                    demo = User(
                        name="demo",
                        first_name="Demo",
                        last_name="User",
                        email="demo@example.com",
                        password_hash=generate_password_hash("password").decode("utf-8"),
                    )
                    db.session.add(demo)
                    db.session.commit()

                today = date.today()

                def add_event_if_missing(title, **kwargs):
                    exists = db.session.scalar(db.select(Event).where(Event.title == title))
                    if exists:
                        return
                    e = Event(owner_id=demo.id, title=title, **kwargs)
                    db.session.add(e)
                    db.session.commit()

                add_event_if_missing(
                    "Underground Rap Night",
                    description="A night for upcoming artists to go head-to-head. Doors 6:30pm.",
                    image_url="img/1.jpg",
                    category="Rap",
                    venue="Central Music Park",
                    artist="Various",
                    date=today + timedelta(days=7),
                    capacity=120,
                    price=Decimal("29.99"),
                )
                add_event_if_missing(
                    "Vibin at the Loft",
                    description="Smooth grooves and late-night jazz standards.",
                    image_url="img/2.jpg",
                    category="Jazz",
                    venue="The Loft",
                    artist="Vibin",
                    date=today + timedelta(days=12),
                    capacity=80,
                    price=Decimal("24.50"),
                )
                add_event_if_missing(
                    "Funky Town",
                    description="Get down with classic soul and funk.",
                    image_url="img/3.jpg",
                    category="Soul",
                    venue="Colters",
                    artist="Funky Town",
                    date=today + timedelta(days=18),
                    capacity=200,
                    price=Decimal("35.00"),
                )
                add_event_if_missing(
                    "Rhythm & Blues",
                    description="R&B showcase with guest vocalists.",
                    image_url="img/4.jpg",
                    category="RnB",
                    venue="The Loft",
                    artist="Various",
                    date=today + timedelta(days=22),
                    capacity=150,
                    price=Decimal("27.00"),
                )
                add_event_if_missing(
                    "Rap Festival",
                    description="Multi-stage hip-hop festival all day.",
                    image_url="img/5.jpg",
                    category="Rap",
                    venue="Central Music Park",
                    artist="Several",
                    date=today + timedelta(days=30),
                    capacity=500,
                    price=Decimal("59.90"),
                )

            app.config["INIT_DONE"] = True

    @app.before_request
    def _init_guard():
        # Lightweight check before each request; runs seeding once
        if not app.config["INIT_DONE"]:
            _ensure_seeded_once()
    
    return app
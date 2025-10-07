from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

SAMPLE_EVENTS = [
    {"title":"Underground Rap night","artist":"Several","date":"22/08/2025","venue":"Central Music Park","category":"Rap","status":"Open","image_url":"/static/img/1.jpg"},
    {"title":"Vibin at the Loft","artist":"Vibin","date":"28/08/2025","venue":"The Loft","category":"Jazz","status":"Open","image_url":"/static/img/2.jpg"},
    {"title":"Funky Town","artist":"Funky Town","date":"11/09/2025","venue":"Colters","category":"Soul","status":"Sold Out","image_url":"/static/img/3.jpg"},
    {"title":"Rhythm & Blues","artist":"Several","date":"14/09/2025","venue":"The Loft","category":"RnB","status":"Open","image_url":"/static/img/4.jpg"},
    {"title":"Rap Festival","artist":"Several","date":"15/09/2025","venue":"Central Music Park","category":"Rap","status":"Cancelled","image_url":"/static/img/5.jpg"},
]

@main_bp.route('/')
def index():
    category = request.args.get("category")
    events = [e for e in SAMPLE_EVENTS if (not category or e["category"] == category)]
    categories = sorted({e["category"] for e in SAMPLE_EVENTS})
    return render_template("events/list.html", events=events, categories=categories, category=category)

@main_bp.route('/me')
@login_required
def me():
    return render_template('user.html', form=None, heading=f"Hello, {current_user.name}")
from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_
from .models import Event, Comment, Order, make_order_id
from .forms import EventForm, CommnetForm, OrderForm
from . import db
from decimal import Decimal


main_bp = Blueprint('main', __name__)


# Main page
@main_bp.route('/')
def index():
    category = request.args.get("category") or None
    q = (request.args.get("q") or "").strip()

    stmt = db.select(Event).order_by(Event.date)
    if category:
        stmt = stmt.where(Event.category == category)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Event.title.ilike(like), Event.venue.ilike(like), Event.artist.ilike(like)))

    events = db.session.scalars(stmt).all()

    categories = db.session.scalars(
        db.select(Event.category).distinct().order_by(Event.category)
    ).all()

    return render_template(
        "events/list.html",
        events=events,
        categories=categories,
        category=category,
        q=q,
    )

#FIX
@main_bp.route('/me')
@login_required
def me():
    return render_template('user.html', form=None, heading=f"Hello, {current_user.name}")


# Event details route
@main_bp.route('/events/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = db.session.get(Event, event_id)
    if not event: abort(404)
    
    comment_form = CommnetForm()
    order_form = OrderForm()

    # Comment post
    if comment_form.submit.data and comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to post a comment.")
            return redirect(url_for('auth.login', next=request.path))
        c = Comment(user_id=current_user.id, event_id=event.id, body=comment_form.body.data.strip())
        db.session.add(c); db.session.commit()
        flash("Comment posted.")
        return redirect(url_for('main.event_detail', event_id=event.id))

    # Booking post
    if order_form.submit.data and order_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to buy tickets.")
            return redirect(url_for('auth.login', next=request.path))

        qty = order_form.qty.data
        # status/stock checks
        if event.cancelled or event.status != "Open":
            flash("This event isn’t open for booking.")
            return redirect(url_for('main.event_detail', event_id=event.id))
        if event.capacity and event.tickets_sold + qty > event.capacity:
            flash("Not enough tickets available.")
            return redirect(url_for('main.event_detail', event_id=event.id))

        unit_price = Decimal(event.price)
        order = Order(
            user_id=current_user.id,
            event_id=event.id,
            qty=qty,
            price=unit_price,
            order_id=make_order_id(event.id),
        )
        event.tickets_sold += qty
        db.session.add(order)
        db.session.commit()
        flash(f"Booking confirmed. Order ID: {order.order_id}")
        return redirect(url_for('main.orders'))

    return render_template('events/detail.html', event=event, comment_form=comment_form, order_form=order_form)



# Event Creation route
@main_bp.route('/events/create', methods=['GET','POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        e = Event(
            owner_id=current_user.id,
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            image_url=(form.image_url.data.strip() if form.image_url.data else None),
            category=form.category.data,
            venue=form.venue.data.strip(),
            artist=form.artist.data.strip(),
            date=form.date.data,
            capacity=form.capacity.data or 0,
            tickets_sold=0,
            price=Decimal(str(form.price.data))
        )
        db.session.add(e)
        db.session.commit()
        flash("Event Created!")
        return redirect(url_for('main.event_detail', event_id=e.id))
    return render_template('events/create.html', form=form)

@ main_bp.route( '/orders')
@login_required
def orders():
    orders = db.session.scalars(
        db.select(Order).where(Order.user_id==current_user.id).order_by(Order.created_at.desc())
    ).all()
    return render_template('orders/list.html', orders=orders)
from . import db
from datetime import datetime, date
from flask_login import UserMixin

#USER
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    #Identity
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    #Profile
    phone = db.Column(db.String(40))
    street_address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #Relationships
    events = db.relationship("Event", backref="owner", lazy=True)
    orders = db.relationship("Order", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

    def __repr__(self):
        return f"<User id={self.id} name={self.name!r}>"
    
#EVENT
class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)

    #owner
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    #event details
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    category =db.Column(db.String(40))
    venue =db.Column(db.String(120))
    artist =db.Column(db.String(120))

    #timing and capacity
    date = db.Column(db.Date, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=0)
    tickets_sold = db.Column(db.Integer, nullable=False, default=0)

    #lifecycle indicators
    cancelled = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #Relationships
    comments = db.relationship("Comment", backref="event", lazy=True, cascade= "all, delete-orphan")
    orders = db.relationship("Order", backref="event", lazy=True, cascade="all, delete-orphan")

    @property
    def status(self) -> str:
        """Assignment-required state: Open / Inactive / Sold Out / Cancelled."""
        if self.cancelled:
            return "Cancelled"
        if self.date < date.today():
            return "Inactive"
        if self.capacity and self.tickets_sold >= self.capacity:
            return "Sold Out"
        return "Open"
    
    def __repr__(self):
        return f"<Event id={self.id} title={self.title!r}>"


#COMMENTS

class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Comment id={self.id} user={self.user_id} event={self.event_id}>"
    

#Order
class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    qty = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(8, 2))

    order_id = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Order id ={self.id} order_id={self.order_id!r}>"

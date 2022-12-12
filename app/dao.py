from app.models import Category, Flight, User, Receipt, ReceiptDetails
from app import db
from flask_login import current_user
from sqlalchemy import func
import hashlib
from datetime import datetime


def load_categories():
    return Category.query.all()


def load_flights(depart=None, arrival=None, time=None):
    query = Flight.query

    if depart:
        query = query.filter(Flight.depart.__eq__(depart))

    if arrival:
        query = query.filter(Flight.arrival.__eq__(arrival))

    if time:
        query = query.filter(Flight.time.__eq__(time))

    # if hangve:
    #     query = query.filter(Flight.time.__eq__(time))

    return query.all()


def get_product_by_id(flight_id):
    return Flight.query.get(flight_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for f in cart.values():
            d = ReceiptDetails(quantity=f['quantity'], price=f['price'] ,
                               receipt=r, flight_id=f['id'])
            db.session.add(d)

        try:
            db.session.commit()
        except:
            return False
        else:
            return True


def count_Flight_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Flight.id))\
                     .join(Flight, Flight.category_id.__eq__(Category.id), isouter=True)\
                     .group_by(Category.id).order_by(Category.id).all()


def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(Flight.id, Flight.name, func.sum(ReceiptDetails.price*ReceiptDetails.quantity), ReceiptDetails.quantity)\
                      .join(ReceiptDetails, ReceiptDetails.flight_id.__eq__(Flight.id))\
                      .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if kw:
        query = query.filter(Flight.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Flight.id).all()


if __name__ == '__main__':
    from app import app
    with app.app_context():
        print(stats_revenue())

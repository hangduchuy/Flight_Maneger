from typing import Any

from flask import render_template, request, redirect, session, jsonify
from app import app, dao, utils
from flask_login import login_user, logout_user, login_required
import cloudinary.uploader
from app.decorators import annonymous_user
from datetime import datetime, timedelta


def index():
    depart = request.args.get('depart')
    arrival = request.args.get('arrival')
    hangve = request.args.get('hangve')
    time = request.args.get('time')
    # dt = datetime.strptime(time, '%Y-%m-%d') + timedelta(hours=12)
    flights = dao.load_flights(depart=depart, arrival=arrival, time=time)

    return render_template('index.html', flights=flights, depart=depart, arrival=arrival, hangve=hangve)


def product_detail(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']

        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=request.form['password'],
                             avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@annonymous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)

            u = request.args.get('next')
            return redirect(u if u else '/')

    return render_template('login.html')


def logout_my_user():
    logout_user()
    return redirect('/login')


def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


def booking():
    return render_template('booking.html')


def add_to_booking():
    data = request.json
    id = str(data['id'])

    key = app.config['CART_KEY']
    booking = session[key] if key in session else {}

    name = data['name']
    price = data['price']

    booking[id] = {
        "id": id,
        "name": name,
        "price": price,
    }

    session[key] = booking
    return jsonify(utils.cart_stats(booking))


def cart():
    return render_template('cart.html')


def add_to_cart():
    data = request.json
    id = str(data['id'])

    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        name = data['name']
        price = data['price']

        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1,
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def update_cart(flight_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and flight_id in cart:
        quantity = int(request.json['quantity'])
        cart[flight_id]['quantity'] = quantity

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


def delete_cart(flight_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and flight_id in cart:
        del cart[flight_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@login_required
def pay():
    err_msg = ''
    key = app.config['CART_KEY']
    cart = session.get(key)

    if dao.add_receipt(cart=cart):
        del session[key]
    else:
        err_msg = 'Đã có lỗi xảy ra!'

    return jsonify({'err_msg': err_msg})
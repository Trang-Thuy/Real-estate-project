from market import app
from flask import render_template, redirect, url_for, flash, request,jsonify,session
from market.models import Item, User, Home, CartItem, Realtor
from market.forms import RegisterForm, LoginForm, SearchForm, SearchContactForm, MyCartTypeForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
import plotly.graph_objects as go
from market import db
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

from market.controller.market_controller import MarketController
from market.controller.auth_controller import AuthController
from market.controller.realtor_controller import RealtorController

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/get_districts', methods=['GET'])
def get_districts():
    city = request.args.get('city')  
    if city:
        # Fetch unique districts based on the selected city
        unique_districts = list(set([item.district for item in Home.query.filter_by(province=city).all()]))
        return jsonify({'districts': unique_districts})
    else:
        return jsonify({'districts': []})
    
@app.route('/market',methods=['GET','POST'])
def market_page():
    if request.method == "POST":
        search_form_data = request.form
        return MarketController.search_market(search_form_data)
     
    if request.method == "GET":
        return MarketController.get_market()
    

@app.route('/market/home_id=<int:home_id>', methods=['GET'])
def get_home(home_id):
    return MarketController.get_home_info(home_id)

@app.route('/add_to_cart/<int:home_id>', methods=['POST'])
@login_required
def add_to_cart(home_id):
    session['search_executed'] -= 1
    current_page_url = request.form.get('current_page_url', '/')
    home = Home.query.get_or_404(home_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, home_id=home.id).first()
    new_cart_item = CartItem(user_id=current_user.id, home_id=home.id)
    if cart_item:        
        flash(f"{home.title} already in your cart", category="danger")
    else:
        new_cart_item.add()
        flash(f"You are successly haved add {home.title} to your cart!", category="success")
    return redirect(current_page_url)

@app.route('/delete_to_cart/<int:home_id>', methods=['POST'])
@login_required
def delete_to_cart(home_id):
    home = Home.query.get_or_404(home_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, home_id=home.id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        
        flash(f"You just deleted {home.title} from your cart", category="success")
    else:
        flash(f"Item not found in your cart", category="danger")
    return redirect(url_for('my_cart'))

@app.route('/mycart', methods=['GET','POST'])
def my_cart():
    my_cart_form = MyCartTypeForm()
    is_saler_page= False
    cart_items=[]
    is_cart_page = True
    if request.method =="POST":
        if my_cart_form.validate_on_submit():
            product_type = my_cart_form.producttype
            if 'home' in product_type:
                cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
                home_ids = [item.home_id for item in cart_items]
                results = Home.query.filter(Home.id.in_(home_ids)).all()
                is_saler_page = False
                cart_items = results
            else:
                cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
                realtor_ids = [item.realtor_id for item in cart_items]
                results = Realtor.query.filter(Realtor.id.in_(realtor_ids)).all()
                is_saler_page = True
                cart_items = results

            if cart_items:
                is_cart_page = True
                return render_template('market.html', items=cart_items, cart_page=is_cart_page,is_saler_page=is_saler_page, my_cart_form=my_cart_form)
            else:
                # is_cart_page = True
                flash("There're no items in your cart", category="danger")
                return redirect(url_for('market_page'))
        # return redirect(url_for('market_page'))
        return render_template('market.html', items=cart_items, cart_page=is_cart_page,is_saler_page=is_saler_page,my_cart_form=my_cart_form)
    if request.method =="GET":
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        home_ids = [item.home_id for item in cart_items]
        results = Home.query.filter(Home.id.in_(home_ids)).all()
        is_saler_page = False
        cart_items = results
        if cart_items:
                is_cart_page = True
                return render_template('market.html', items=cart_items, cart_page=is_cart_page,is_saler_page=is_saler_page, my_cart_form=my_cart_form)

@app.route('/register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)

        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as: {user_to_create.username}',category='success')
        
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error: {err_msg}',category='danger')

    return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    login_form_data = request.get_json()
    return AuthController.login(login_form_data)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))

@app.route('/saler',methods=['GET','POST'])
def realtor_page():
    search_contact_form = SearchContactForm()
    if request.method == "POST":
        if search_contact_form.validate_on_submit():
            name = search_contact_form.contact_name.data
            phone = search_contact_form.contact_phone.data
            results = Realtor.query.filter((Realtor.contact_name.contains(name))&(Realtor.contact_phone.contains(phone)) ).all()
            if results:
                is_cart_page = False
                is_saler_page = True
                return render_template('realtor.html', items=results,art_page=is_cart_page,is_saler_page=is_saler_page,form=search_contact_form)
            else:
                flash('There are no results matching your search', category='danger')
        return redirect(url_for('realtor_page'))

    if request.method == "GET":
        return RealtorController.get_all_realtor()

@app.route('/saler/realtor_id=<int:realtor_id>', methods=['GET'])
def get_realtor_info(realtor_id):
    return RealtorController.get_realtor_info(realtor_id)

@app.route('/add_to_cart_realtor/<int:realtor_id>', methods=['POST'])
@login_required
def add_to_cart_realtor(realtor_id):
    return RealtorController.add_to_cart_realtor(realtor_id, current_user);


@app.route('/delete_to_cart_realtor/<int:realtor_id>', methods=['POST'])
@login_required
def delete_to_cart_realtor(realtor_id):
    return RealtorController.add_to_cart_realtor(realtor_id, current_user)

# @app.route('/visualize_page')
# def visualize_page():
#     homes = Home.query.all()
#     # Extract some data from the Home objects
#     data = [{'x': home.province, 'y': home.price} for home in homes]

#     # Create a plot using plotly.graph_objects
#     fig = go.Figure(data=[go.Bar(x=d['x'], y=d['y']) for d in data])

#     # Render the plot in a template
#     return render_template('visualize.html', fig=fig)

@app.route('/visualize_page')
def visualize():
    provinces = db.session.query(Home.province, db.func.count(Home.id), db.func.avg(Home.price)).group_by(Home.province).all()
    fig_data = [{'type': 'bar', 'x': [province[0] for province in provinces], 'y': [province[1] for province in provinces], 'name': 'Number of Homes'},
                {'type': 'bar', 'x': [province[0] for province in provinces], 'y': [province[2] for province in provinces], 'name': 'Average Price'}]
    fig_layout = {
        'title': 'Statistics by Province',
        'xaxis': {'title': 'Province'},
        'yaxis': {'title': 'Value'}
    }

    fig_json = json.dumps({'data': fig_data, 'layout': fig_layout})
    return render_template('plot.html', fig_json=fig_json)
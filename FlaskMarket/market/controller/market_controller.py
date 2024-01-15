from flask import session, jsonify
from market.models import Home
import json

def get_market():
    items = Home.query.all()
    session['search_executed'] = 2
    if 'search_executed' in session and session['search_executed']<=2:
        if 'search_results' in session:
            result_ids = [item[0] for item in session['search_results']]
            items = Home.query.filter(Home.id.in_(result_ids)).all()
        items = Home.query.all()
    is_cart_page = False
    is_saler_page = False
    
    for i, home in enumerate(items):
        items[i] = home.to_dict()

    return jsonify({
        'items' : items,
        'cart_page': is_cart_page,
        'is_saler_page': is_saler_page
    })

def search_market(search_form):
    city = search_form['city']
    district = search_form['district']
    price = search_form['price']
    square = search_form['square']

    results = Home.query.filter((Home.province.contains(city)) &
        (Home.district.contains(district)) &
        (Home.price < price) &
        (Home.square < square)
    ).all()

    for i, home in enumerate(results):
        results[i] = home.to_dict()


    if results:
        is_cart_page = False
        is_saler_page = False
        return jsonify({
            'items' :results,
            'cart_page': is_cart_page,
            'is_saler_page': is_saler_page
        }), 200
    else:
        return jsonify({
            'message': 'There are no results matching your search'
        }), 404

def get_home_info(home_id):
    home : Home = Home.query.filter_by(id=home_id).first()
    if home:
        return jsonify(home.to_dict()), 200
    else:
        return jsonify({
            'message' : "Not found"
        }), 404
from flask import session, jsonify
from market.forms_validate.market.search_market import MarketSearchForm
from market.models import Home
import json

class MarketController:
    @staticmethod
    def get_market():
        items = Home.query.all()
        if 'search_executed' in session and session['search_executed']<=2:
            if 'search_results' in session:
                result_ids = [item[0] for item in session['search_results']]
                items = Home.query.filter(Home.id.in_(result_ids)).all()
            items = Home.query.all()
        
        for i, home in enumerate(items):
            items[i] = home.to_dict()

        return jsonify({
            'items' : items,
        })

    @staticmethod
    def search_market(form_data):
        print(form_data)
        search_form = MarketSearchForm(form_data)

        if search_form.validate():
            city = search_form.city.data
            district = search_form.district.data
            price = search_form.price.data
            square = search_form.square.data

            results = Home.query.filter((Home.province.contains(city)) &
                (Home.district.contains(district)) &
                (Home.price < price) &
                (Home.square < square)
            ).all()

            for i, home in enumerate(results):
                results[i] = home.to_dict()


            if results:
                return jsonify({
                    'items' :results,
                }), 200
            else:
                return jsonify({
                    'message': 'There are no results matching your search'
                }), 404
        else:
            return jsonify({
                'error' : search_form.errors
            }), 400

    @staticmethod
    def get_home_info(home_id):
        home : Home = Home.query.filter_by(id=home_id).first()
        if home:
            return jsonify(home.to_dict()), 200
        else:
            return jsonify({
                'message' : "Not found"
            }), 404
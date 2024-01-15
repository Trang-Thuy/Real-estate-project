
from flask import jsonify
from market.models import CartItem, Realtor
from market import db


def RealtorController_add_to_cart_realtor(realtor_id, current_user):
    realtor = Realtor.query.get_or_404(realtor_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, realtor_id=realtor.id).first()
    new_cart_item = CartItem(user_id=current_user.id, realtor_id=realtor.id)

    if cart_item:        
        return jsonify({'message' : f"{realtor.contact_name} already in your cart"}), 203
    else:
        new_cart_item.add()
        return jsonify(f"You are successly haved add {realtor.contact_name} to your cart!", category="success"), 200

def RealtorController_delete_to_card(realtor_id, current_user):
    realtor = Realtor.query.get_or_404(realtor_id)
    cart_item = CartItem.query.filter_by(user_id=current_user.id, realtor_id=realtor.id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        
        jsonify({'message' : f"You just deleted {realtor.contact_name} from your cart"}), 200
    else:
        jsonify({'message' f"Item not found in your cart"}), 200

def RealtorController_get_realtor_info(realtor_id):
    realtor = Realtor.query.filter_by(id=realtor_id).first()
    if realtor:
        return jsonify(realtor.to_dict()), 200
    else:
        return jsonify({"message" : "Not found"}), 200

def RealtorController_get_all_realtor():
    salers = Realtor.query.all()

    for i, saler in enumerate(salers):
        saler[i] = saler.to_dict()

    is_cart_page = False
    is_saler_page= True
    return jsonify({
        'salers' : salers,
        'is_cart_page' : is_cart_page,
        'is_saler_page' : is_saler_page
    })
from market import db
from market import bcrypt
from market import login_manager
from flask_login import UserMixin

# with app.app_context():
#     db.create_all()

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address=db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(),nullable=False,default=1000)
    items = db.relationship('Item', backref='owned_user',lazy=True)
    cart = db.relationship('CartItem', backref='user_cart', lazy=True)

    
    @property
    def prettier_budget(self):
        if len(str(self.budget))>=4:
              return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
             return f"{self.budget}$"

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
            self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self, item_obj):
         return item_obj in self.items
    
    
        
class Item(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode=db.Column(db.String(length=12),nullable=False,unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description=db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    def __repr__(self):
        return f'Item{self.name}'
    
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self,user):
         self.owner=None
         user.budget += self.price
         db.session.commit()
    
class Home(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(length=300), nullable=False)
    price = db.Column(db.Integer(),nullable=False)
    square = db.Column(db.Integer(), nullable=False)
    address=db.Column(db.String(length=1024), nullable=False)
    street = db.Column(db.Integer())
    ward = db.Column(db.String(length=300))
    province = db.Column(db.String(length=300))
    district = db.Column(db.String(length=300))
    count = db.Column(db.Integer(),nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'square': self.square,
            'address': self.address,
            'street': self.street,
            'ward': self.ward,
            'province': self.province,
            'district': self.district,
            'count': self.count
        }

     

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=True)
    realtor_id = db.Column(db.Integer, db.ForeignKey('realtor.id'), nullable=True)
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Realtor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(length=300), nullable=False)
    contact_phone = db.Column(db.Integer(), nullable=False)
    cart = db.relationship('CartItem', backref='saler_cart', lazy=True)

    def to_dict(self):
        return {
            'contact_name' : self.contact_name,
            'contact_phone' : self.contact_phone
        }


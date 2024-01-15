from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User, Item, Home
from flask import current_app
from market import db


class RegisterForm(FlaskForm):
    # def validate_on_submit(self, extra_validators=None):
    #     return super().validate_on_submit(extra_validators)
    #check if username existing or not
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Try a different username')
    
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Try a different email address')
        
    
    username = StringField(label='User Name:', validators=[Length(min=2,max=30), DataRequired()])
    email_address= StringField(label='Email Address',validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Password:',validators=[Length(min=6),DataRequired()])
    #verify pw2 match pw1
    password2 = PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Submit to Create Account')

class LoginForm(FlaskForm):
    username=StringField(label="Enter your username:",validators=[DataRequired()])
    password = StringField(label="Password",validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

# class PurchaseItemForm(FlaskForm):
#     submit = SubmitField(label="Purchase Item!")

# class SellItemForm(FlaskForm):
#     submit = SubmitField(label="Sell Item!")
# class SavetoListForm(FlaskForm):
#     submit = SubmitField(label="Save")
class SearchForm(FlaskForm):
    city = SelectField('City',render_kw={"class": "form-control", "multiple": "multiple"})
    district = SelectField('District', coerce=str,render_kw={"class": "form-control", "multiple": "multiple"})
    price = SelectField('Price Range', choices=[(str(i), str(i)) for i in range(1000, 5000, 1000)])
    square = StringField('Square')
    submit = SubmitField('Search')
    def __init__(self, json_data = None, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.city.choices = [(item.province, item.province) for item in Home.query.all()]
        self.city.choices = list(set(self.city.choices))

        if self.city.data:
            self.district.choices = [(item.district, item.district) for item in Home.query.filter_by(province=self.city.data).all()]
    def to_dict(self):
        return {
            'city': self.city.data,
            'district': self.district.data,
            'price': self.price.data,
            'square': self.square.data
        }

class SearchContactForm(FlaskForm):
    contact_name = StringField('Name')
    contact_phone = StringField('Phone')
    submit = SubmitField('Search')

class MyCartTypeForm(FlaskForm):
    producttype = SelectField('Select', choices=[('Home', 'Home'), ('Realtor', 'Realtor')] )
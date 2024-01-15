from wtforms import Form, StringField, IntegerField, validators

class MarketSearchForm(Form):
    city = StringField('City', [validators.DataRequired()])
    district = StringField('District', [validators.DataRequired()])
    price = IntegerField('Price', [validators.NumberRange(min=0), validators.DataRequired()])
    square = IntegerField('Square', [validators.NumberRange(min=0), validators.DataRequired()])
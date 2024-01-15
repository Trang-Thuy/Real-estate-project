
from wtforms import Form, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from market.models import User


class RegisterForm(Form):
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
        
    
    username = StringField(label='User Name:', validators=[Length(min=2,max=30), DataRequired(), validate_username()])
    email_address= StringField(label='Email Address',validators=[Email(),DataRequired(), validate_email_address()])
    password1 = PasswordField(label='Password:',validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price per kg', validators=[DataRequired(), NumberRange(min=0.01)])
    quantity = FloatField('Available Quantity (kg)', validators=[DataRequired(), NumberRange(min=0.1)])
    category = SelectField('Category', choices=[
        ('paddy', 'Paddy'),
        ('rice', 'Rice'),
        ('wheat', 'Wheat'),
        ('barley', 'Barley'),
        ('corn', 'Corn'),
        ('millet', 'Millet'),
        ('oats', 'Oats'),
        ('other', 'Other')
    ])
    submit = SubmitField('Save Product')

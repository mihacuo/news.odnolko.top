from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    duration = SelectField(
        'Select Duration',
        choices=[
            (1, '1 Day'),
            (3, '3 Days'),
            (7, '1 Week'),
            (14, '2 Weeks'),
            (30, '1 Month')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Go')
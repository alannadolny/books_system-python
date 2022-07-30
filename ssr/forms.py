from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=20)])
    author = StringField('Author', validators=[DataRequired()])
    image = URLField('Image', validators=[Optional(), URL()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])

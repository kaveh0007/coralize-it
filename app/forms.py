from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length

class IssueForm(FlaskForm):
    issue = TextAreaField("Issue", validators=[InputRequired(), Length(min=30, max=1000)])
    ask = SubmitField("Debug")
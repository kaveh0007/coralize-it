from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length

class IssueForm(FlaskForm):
    repository_name = StringField("Repository Name", validators=[InputRequired()])
    owner_name = StringField("Owner Name", validators=[InputRequired()])
    issue = TextAreaField("Issue", validators=[InputRequired(), Length(min=30, max=1000)])
    ask = SubmitField("Debug")
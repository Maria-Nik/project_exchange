from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField, StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    team_leader = StringField('Team leader', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    work_size = StringField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    content = TextAreaField("Content")
    submit = SubmitField('Send')
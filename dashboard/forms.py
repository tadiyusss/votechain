from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField
from wtforms.validators import DataRequired, Length

class VoteForm(FlaskForm):
    candidates = RadioField('Candidate', choices = [('candidate1', 'Candidate 1'), ('candidate2', 'Candidate 2'), ('candidate3', 'Candidate 3')], validators = [DataRequired()])
    private_key = StringField('Private Key', validators = [DataRequired(), Length(min = 64, max = 64)])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    first_name = StringField('Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    username = StringField('Username', validators = [DataRequired(), Length(min = 4, max = 20)])
    submit = SubmitField('Submit')
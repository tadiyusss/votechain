from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class VoteForm(FlaskForm):
    candidates = RadioField('Candidate', choices = [('candidate1', 'Candidate 1'), ('candidate2', 'Candidate 2'), ('candidate3', 'Candidate 3')], validators = [DataRequired()])
    submit = SubmitField('Submit')


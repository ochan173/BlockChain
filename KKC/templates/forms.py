from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired


class TransactionForm(FlaskForm):
    destinataire = StringField("Destinataire", validators=[DataRequired()])
    montant = FloatField("Montant", validators=[DataRequired()])
    submit = SubmitField('Envoyer')


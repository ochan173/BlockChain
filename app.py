from KKC import action
from KKC.core import app, db, admin
from flask_admin.contrib.sqla import ModelView
from KKC.model import Block, Transaction, get_data

db.create_all()
list = get_data()
db.session.add_all(list)
admin.add_view(ModelView(Block, db.session))
admin.add_view(ModelView(Transaction, db.session))

app.run()


from KKC import action
from KKC.core import app, db, admin
from flask_admin.contrib.sqla import ModelView
from KKC.model import Block, Transaction


data = ["149849198", "28949498498", "39849849841"]
#block = Block("1231dwqwe", data)

db.create_all()
#get_data()
admin.add_view(ModelView(Block, db.session))
admin.add_view(ModelView(Transaction, db.session))

app.run()


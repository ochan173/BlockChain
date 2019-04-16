from KKC.core import app, db, admin
from flask_admin.contrib.sqla import ModelView
from KKC.model import Block


data = ["149849198", "28949498498", "39849849841"]
block = Block("1231dwqwe", data)

db.create_all()
db.session.add(block)
admin.add_view(ModelView(Block, db.session))

app.run()
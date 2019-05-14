from KKC import action
from KKC.core import app, db, admin
from flask_admin.contrib.sqla import ModelView
from KKC.model import Block, Transaction, Contributeur, get_data


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()


db.create_all()

clear_data(db.session)

get_data()

db.session.commit()
admin.add_view(ModelView(Block, db.session))
admin.add_view(ModelView(Transaction, db.session))
admin.add_view(ModelView(Contributeur, db.session))

app.run()



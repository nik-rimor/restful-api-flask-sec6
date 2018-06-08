from src.db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    # 'Backreference' allows the a StoreModel object to see which items are in the items table
    # in the database with store_id equal to the id of this StoreModel object
    # this is a list of items since we have many items -> one store
    # lazy = 'dynamic' prevents the creation of the whole list of item objects as soon as we create
    # a StoreModel object. It changes the self.items from list to a query builder that we are going
    # to execute when we want to retrieve the list ( self.items.all() )
    items = db.relationship('ItemModel', lazy = 'dynamic')

    def __init__(self, name, _id = None):
        self.name = name
        self.id = _id

    def json(self):
        return {
            "store_id": int(self.id),
            "name": self.name,
            "items": [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first() #SELECT * FROM __tablename__ WHERE name=name LIMIT 1


    def save_to_db(self):    #upserting method
        # SQLAlchemy can translate directly form object to row
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

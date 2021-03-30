from db import db
import datetime


class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    part = db.Column(db.String(100), db.ForeignKey('part_numbers.part_number'))
    category = db.Column(db.String(100), db.ForeignKey('categories.category'))
    purchase_price = db.Column(db.Float(precision=2))
    sale_price = db.Column(db.Float(precision=2))

    purchase_detail = db.relationship('PurchaseDetailModel')

    def __init__(self, part, category, purchase_price, sale_price):
        aux = ProductModel.query.all()

        self.part = part
        self.category = category
        self.purchase_price = purchase_price
        self.sale_price = sale_pric

    def json(self):
        return {'id': self.id,
                'part': self.part,
                'category': self.category,
                'purchase_price': self.purchase_price,
                'sale_price': self.sale_price
                }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

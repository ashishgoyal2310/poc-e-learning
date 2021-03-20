from models.database import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(
        db.DateTime,
        nullable=False
    )
    date_updated = db.Column(
        db.DateTime,
        nullable=False
    )
    description = db.Column(
        db.String(255),
        nullable=True
    )
    image_path = db.Column(
        db.String(100),
        nullable=True
    )
    on_discount = db.Column(
        db.Boolean,
        nullable=False
    )
    discount_price = db.Column(
        db.Float(precision=2, asdecimal=True),
        nullable=False
    )
    price = db.Column(
        db.Float(precision=2, asdecimal=True),
        nullable=False
    )
    title = db.Column(
        db.String(100),
        nullable=False
    )

    def __repr__(self):
        return '<Course %r>' % self.title
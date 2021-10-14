from snap_shopusingai.project import db


class ColorVO(db.Model):
    __tablename__ = 'colormaster'
    colorId = db.Column('colorId', db.Integer, primary_key=True, autoincrement=True)
    colorName = db.Column('colorName', db.String(100))
    colorHexcode = db.Column('colorHexcode', db.String(100))

    def as_dict(self):
        return {
            'colorId': self.colorId,
            'colorName': self.colorName,
            'colorHexcode': self.colorHexcode
        }


db.create_all()

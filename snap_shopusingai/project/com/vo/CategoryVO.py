from snap_shopusingai.project import db


class CategoryVO(db.Model):
    __tablename__ = 'categorymaster'
    categoryId = db.Column('categoryId', db.Integer, primary_key=True, autoincrement=True)
    categoryName = db.Column('categoryName', db.String(100))
    categoryDescription = db.Column('categoryDescription', db.String(100))

    def as_dict(self):
        return {
            'categoryId': self.categoryId,
            'categoryName': self.categoryName,
            'categoryDescription': self.categoryDescription
        }


db.create_all()

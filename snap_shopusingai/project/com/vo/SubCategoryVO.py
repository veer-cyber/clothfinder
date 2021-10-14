from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.CategoryVO import CategoryVO


class SubCategoryVO(db.Model):
    __tablename__ = 'subcategorymaster'
    subCategoryId = db.Column('subCategoryId', db.Integer, primary_key=True, autoincrement=True)
    subCategoryName = db.Column('subCategoryName', db.String(100), nullable=False)
    subCategoryDescription = db.Column('subCategoryDescription', db.String(100), nullable=False)
    subCategory_CategoryId = db.Column('subCategory_CategoryId', db.Integer, db.ForeignKey(CategoryVO.categoryId))

    def as_dict(self):
        return {
            'subCategoryId': self.subCategoryId,
            'subCategoryName': self.subCategoryName,
            'subCategoryDescription': self.subCategoryDescription,
            'subCategory_CategoryId': self.subCategory_CategoryId
        }


db.create_all()

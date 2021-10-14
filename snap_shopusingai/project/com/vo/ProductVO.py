from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.CategoryVO import CategoryVO
from snap_shopusingai.project.com.vo.SubCategoryVO import SubCategoryVO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO

class ProductVO(db.Model):
    __tablename__ = 'productmaster'
    productId = db.Column('productId', db.Integer, primary_key=True, autoincrement=True)
    productName = db.Column('productName', db.String(100), nullable=False)
    productDescription = db.Column('productDescription', db.String(100), nullable=False)
    productPrice = db.Column('productPrice', db.Integer, nullable=False)
    productColorName = db.Column('productColorName', db.String(100), nullable=False)
    product_CategoryId = db.Column('product_CategoryId', db.Integer, db.ForeignKey(CategoryVO.categoryId))
    product_SubCategoryId = db.Column('product_SubCategoryId', db.Integer, db.ForeignKey(SubCategoryVO.subCategoryId))
    productFileName = db.Column('productFileName', db.String(100))
    productFilePath = db.Column('productFilePath', db.String(100))
    productSize = db.Column('productSize', db.String(100), nullable=False)
    product_LoginId = db.Column('product_CategoryId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'productId': self.productId,
            'productName': self.productName,
            'productDescription': self.productDescription,
            'productPrice': self.productPrice,
            'productColorCode': self.productColorCode,
            'productCategory_CategoryId': self.productCategory_CategoryId,
            'productSubCategory_subCategoryId': self.productSubCategory_subCategoryId,
            'productFileName': self.productFileName,
            'productFilePath': self.productFilePath,
            'productSize': self.productSize
        }


db.create_all()

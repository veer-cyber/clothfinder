from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.CategoryVO import CategoryVO
from snap_shopusingai.project.com.vo.ProductVO import ProductVO
from snap_shopusingai.project.com.vo.SubCategoryVO import SubCategoryVO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO
from snap_shopusingai.project.com.vo.ShopkeeperVO import ShopkeeperVO


class ProductDAO:
    def insertProduct(self, productVO):
        db.session.add(productVO)
        db.session.commit()

    def viewProduct(self):
        productList = db.session.query(ProductVO, SubCategoryVO, CategoryVO).join(SubCategoryVO,
                                                                                  ProductVO.product_SubCategoryId == SubCategoryVO.subCategoryId).join(
            CategoryVO, ProductVO.product_CategoryId == CategoryVO.categoryId).all()

        return productList

    def deleteProduct(self, productId):
        productList = ProductVO.query.get(productId)

        db.session.delete(productList)

        db.session.commit()
        return productList

    def editProduct(self, productVO):
        productList = ProductVO.query.filter_by(productId=productVO.productId).all()

        return productList

    def updateProduct(self, productVO):
        db.session.merge(productVO)

        db.session.commit()

    def getSpecificProduct(self, productVO):
        print(ProductVO.productFileName)
        productList = db.session.query(ProductVO, LoginVO, ShopkeeperVO).filter(ProductVO.productFileName==productVO.productFileName).join(LoginVO,ProductVO.product_LoginId == LoginVO.loginId).join(ShopkeeperVO,ShopkeeperVO.shopkeeper_LoginId == LoginVO.loginId).all()
        print(productList)

        return productList
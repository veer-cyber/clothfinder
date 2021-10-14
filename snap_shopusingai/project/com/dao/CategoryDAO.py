from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.CategoryVO import CategoryVO


class CategoryDAO:
    def insertCategory(self, categoryVO):
        db.session.add(categoryVO)
        db.session.commit()

    def viewCategory(self):
        categoryList = CategoryVO.query.all()

        return categoryList

    def deleteCategory(self, categoryVO):
        categoryList = CategoryVO.query.get(categoryVO.categoryId)

        db.session.delete(categoryList)

        db.session.commit()

    def editCategory(self, categoryVO):
        categoryList = CategoryVO.query.filter_by(categoryId=categoryVO.categoryId).all()

        return categoryList

    def updateCategory(self, categoryVO):
        db.session.merge(categoryVO)

        db.session.commit()

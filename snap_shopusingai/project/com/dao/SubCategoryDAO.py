from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.CategoryVO import CategoryVO
from snap_shopusingai.project.com.vo.SubCategoryVO import SubCategoryVO


class SubCategoryDAO:
    def insertSubCategory(self, subCategoryVO):
        db.session.add(subCategoryVO)
        db.session.commit()

    def viewSubCategory(self):
        subCategoryList = db.session.query(SubCategoryVO, CategoryVO).join(CategoryVO,
                                                                           SubCategoryVO.subCategory_CategoryId == CategoryVO.categoryId).all()

        return subCategoryList

    def deleteSubCategory(self, subCategoryId):
        subCategoryList = SubCategoryVO.query.get(subCategoryId)

        db.session.delete(subCategoryList)

        db.session.commit()

    def editSubCategory(self, subCategoryVO):
        subCategoryList = SubCategoryVO.query.filter_by(subCategoryId=subCategoryVO.subCategoryId)

        return subCategoryList

    def updateSubCategory(self, subCategoryVO):
        db.session.merge(subCategoryVO)

        db.session.commit()

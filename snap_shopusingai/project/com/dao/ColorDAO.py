from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.ColorVO import ColorVO


class ColorDAO:
    def insertColor(self, colorVO):
        db.session.add(colorVO)
        db.session.commit()

    def viewColor(self):
        colorList = ColorVO.query.all()

        return colorList

    def deleteColor(self, colorVO):
        colorList = ColorVO.query.get(colorVO.colorId)

        db.session.delete(colorList)

        db.session.commit()

    def editColor(self, colorVO):
        colorList = ColorVO.query.filter_by(colorId=colorVO.colorId).all()

        return colorList

    def updateColor(self, colorVO):
        db.session.merge(colorVO)

        db.session.commit()

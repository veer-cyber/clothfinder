from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.ImageVO import ImageVO


class ImageDAO:
    def insertImage(self, imageVO):
        db.session.add(imageVO)
        db.session.commit()

    def viewImage(self):
        imageList = ImageVO.query.all()
        return imageList

    def deleteImage(self, imageVO):
        imageList = ImageVO.query.get(imageVO.imageId)
        db.session.delete(imageList)
        db.session.commit()

        return imageList

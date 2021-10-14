from snap_shopusingai.project import db


class ImageVO(db.Model):
    __tablename__ = 'imagemaster'
    imageId = db.Column('imageId', db.Integer, primary_key=True, autoincrement=True)
    imageFileName = db.Column('imageFileName', db.String(100))
    imageFilePath = db.Column('imageFilePath', db.String(100))
    imageUploadDate = db.Column('imageUploadDate', db.String(100))
    imageUploadTime = db.Column('imageUploadTime', db.String(100))

    def as_dict(self):
        return {
            'imageId': self.imageId,
            'imageFileName': self.imageFileName,
            'imageFilePath': self.imageFilePath,
            'imageUploadDate': self.imageUploadDate,
            'imageUploadTime': self.imageUploadTime
        }


db.create_all()

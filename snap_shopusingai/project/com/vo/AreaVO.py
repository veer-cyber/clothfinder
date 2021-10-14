from snap_shopusingai.project import db


class AreaVO(db.Model):
    __tablename__ = 'areamaster'
    areaId = db.Column('areaId', db.Integer, primary_key=True, autoincrement=True)
    areaName = db.Column('areaName', db.String(100))
    areaPincode = db.Column('areaPincode', db.String(6))

    def as_dict(self):
        return {
            'areaId': self.areaId,
            'areaName': self.areaName,
            'areaPincode': self.areaPincode
        }


db.create_all()

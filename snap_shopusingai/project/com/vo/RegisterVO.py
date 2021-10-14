from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.AreaVO import AreaVO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO


class RegisterVO(db.Model):
    __tablename__ = 'registermaster'
    registerId = db.Column('registerId', db.Integer, primary_key=True, autoincrement=True)
    registerFullName = db.Column('registerFullName', db.String(100), nullable=False)
    registerAddress = db.Column('registerAddress', db.String(100), nullable=False)
    registerContact = db.Column('registerContact', db.String(100), nullable=False)
    register_AreaId = db.Column('register_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    register_LoginId = db.Column('register_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'registerId': self.registerId,
            'registerFullName': self.registerFullName,
            'registerAddress': self.registerAddress,
            'registerContact': self.registerContact,
            'register_AreaId': self.register_AreaId,
            'register_LoginId': self.register_LoginId
        }


db.create_all()

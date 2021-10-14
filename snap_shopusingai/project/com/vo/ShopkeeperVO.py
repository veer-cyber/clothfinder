from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.AreaVO import AreaVO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO


class ShopkeeperVO(db.Model):
    __tablename__ = 'shopkeepermaster'
    shopkeeperId = db.Column('shopkeeperId', db.Integer, primary_key=True, autoincrement=True)
    shopkeeperShopName = db.Column('shopkeeperShopName', db.String(100), nullable=False)
    shopkeeperFullName = db.Column('shopkeeperFullName', db.String(100), nullable=False)
    shopkeeperAddress = db.Column('shopkeeperAddress', db.String(100), nullable=False)
    shopkeeperContact = db.Column('shopkeeperContact', db.String(100), nullable=False)
    shopkeeper_AreaId = db.Column('shopkeeper_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    shopkeeper_LoginId = db.Column('shopkeeper_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'shopkeeperId': self.shopkeeperId,
            'shopkeeperShopName': self.shopkeeperShopName,
            'shopkeeperFullName': self.shopkeeperFullName,
            'shopkeeperAddress': self.shopkeeperAddress,
            'shopkeeperContact': self.shopkeeperContact,
            'shopkeeper_AreaId': self.shopkeeper_AreaId,
            'shopkeeper_LoginId': self.shopkeeper_LoginId
        }


db.create_all()

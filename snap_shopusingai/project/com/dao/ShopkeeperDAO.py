from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.AreaVO import AreaVO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO
from snap_shopusingai.project.com.vo.ShopkeeperVO import ShopkeeperVO


class ShopkeeperDAO:
    def insertShopkeeper(self, shopkeeperVO):
        db.session.add(shopkeeperVO)

        db.session.commit()

    def viewShopkeeper(self):
        shopkeeperList = db.session.query(ShopkeeperVO, AreaVO, LoginVO).join(AreaVO,
                                                                              ShopkeeperVO.shopkeeper_AreaId == AreaVO.areaId).join(
            LoginVO, ShopkeeperVO.shopkeeper_LoginId == LoginVO.loginId).all()

        return shopkeeperList

    def viewShopkeeperIndex(self):
        shopkeeperList = db.session.query(ShopkeeperVO, LoginVO).join(LoginVO,
                                                                      ShopkeeperVO.shopkeeper_LoginId == LoginVO.loginId).all()

        return shopkeeperList

    def validateLogin(self, loginId):
        loginList = LoginVO.query.filter_by(loginId=loginId)

        return loginList

    def manageShopkeeper(self, loginVO):
        db.session.merge(loginVO)

        db.session.commit()

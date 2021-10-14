from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.AreaVO import AreaVO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO
from snap_shopusingai.project.com.vo.RegisterVO import RegisterVO


class RegisterDAO:
    def insertRegister(self, registerVO):
        db.session.add(registerVO)

        db.session.commit()

    def viewRegister(self):
        registerList = db.session.query(RegisterVO, AreaVO, LoginVO).join(AreaVO,
                                                                          RegisterVO.register_AreaId == AreaVO.areaId).join(
            LoginVO, RegisterVO.register_LoginId == LoginVO.loginId).all()

        return registerList

    def validateLogin(self, loginId):
        loginList = LoginVO.query.filter_by(loginId=loginId)

        return loginList

    def manageUser(self, loginVO):
        db.session.merge(loginVO)

        db.session.commit()

    def viewUserIndex(self):
        registerList = db.session.query(RegisterVO, LoginVO).join(LoginVO,
                                                                  RegisterVO.register_LoginId == LoginVO.loginId).all()

        return registerList

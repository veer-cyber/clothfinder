from snap_shopusingai.project import db
from snap_shopusingai.project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername, loginPassword=loginVO.loginPassword)

        return loginList

    def insertLogin(self, LoginVO):
        db.session.add(LoginVO)
        db.session.commit()

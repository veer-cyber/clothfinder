import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, redirect, url_for

from snap_shopusingai.project import app
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from snap_shopusingai.project.com.dao.AreaDAO import AreaDAO
from snap_shopusingai.project.com.dao.LoginDAO import LoginDAO
from snap_shopusingai.project.com.dao.RegisterDAO import RegisterDAO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO
from snap_shopusingai.project.com.vo.RegisterVO import RegisterVO


@app.route('/user/loadRegister', methods=['GET'])
def userLoadRegister():
    try:
        areaDAO = AreaDAO()
        areaVOList = areaDAO.viewArea()

        return render_template('user/register.html', areaVOList=areaVOList)
    except Exception as ex:
        print(ex)


@app.route('/user/insertRegister', methods=['POST'])
def userInsertRegister():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        loginUsername = request.form['loginUsername']

        registerFullName = request.form['registerFullName']
        register_AreaId = request.form['register_AreaId']
        registerAddress = request.form['registerAddress']
        registerContact = request.form['registerContact']

        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        print("loginPassword=" + loginPassword)

        sender = "snapshop0412@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "LOGIN PASSWORD"

        msg.attach(MIMEText('Your Password is:' + loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "Qwer123@")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "user"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin(loginVO)

        registerVO.registerFullName = registerFullName
        registerVO.register_AreaId = register_AreaId
        registerVO.registerAddress = registerAddress
        registerVO.registerContact = registerContact
        registerVO.register_LoginId = loginVO.loginId

        registerDAO.insertRegister(registerVO)

        server.quit()

        return render_template("admin/login.html")

    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard')
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':

            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewUserIndex()

            return render_template('user/index.html', registerVOList=registerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser')
def adminViewUser():
    try:
        if adminLoginSession() == 'admin':

            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewRegister()

            return render_template('admin/viewUser.html', registerVOList=registerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/manageUser')
def adminManageUser():
    try:
        if adminLoginSession() == 'admin':

            loginId = request.args.get('loginId')

            loginVO = LoginVO()
            registerDAO = RegisterDAO()

            loginVOList = registerDAO.validateLogin(loginId)

            loginDictList = [i.as_dict() for i in loginVOList]
            print(loginDictList)

            if loginDictList[0]['loginStatus'] == "active":

                loginStatus = "inactive"

                loginVO.loginId = loginId
                loginVO.loginStatus = loginStatus

                registerDAO.manageUser(loginVO)

                return redirect(url_for("adminViewUser"))

            elif loginDictList[0]['loginStatus'] == "inactive":

                loginStatus = "active"

                loginVO.loginId = loginId
                loginVO.loginStatus = loginStatus

                registerDAO.manageUser(loginVO)

                return redirect(url_for("adminViewUser"))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

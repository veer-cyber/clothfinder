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
from snap_shopusingai.project.com.dao.ShopkeeperDAO import ShopkeeperDAO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO
from snap_shopusingai.project.com.vo.ShopkeeperVO import ShopkeeperVO


@app.route('/shopkeeper/loadRegister', methods=['GET'])
def shopkeeperLoadRegister():
    try:
        areaDAO = AreaDAO()
        areaVOList = areaDAO.viewArea()

        return render_template('shopkeeper/register.html', areaVOList=areaVOList)
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/insertRegister', methods=['POST'])
def shopkeeperInsertRegister():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        shopkeeperVO = ShopkeeperVO()
        shopkeeperDAO = ShopkeeperDAO()

        loginUsername = request.form['loginUsername']

        shopkeeperShopName = request.form['shopkeeperShopName']
        shopkeeperFullName = request.form['shopkeeperFullName']
        shopkeeper_AreaId = request.form['shopkeeper_AreaId']
        shopkeeperAddress = request.form['shopkeeperAddress']
        shopkeeperContact = request.form['shopkeeperContact']

        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        print("loginPassword=" + loginPassword)

        sender = "snapshop0412@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        print("###############################################################")
        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "LOGIN PASSWORD"

        msg.attach(MIMEText('Your Password is:' + loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "Qwer123@")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "shopkeeper"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin(loginVO)

        shopkeeperVO.shopkeeperShopName = shopkeeperShopName
        shopkeeperVO.shopkeeperFullName = shopkeeperFullName
        shopkeeperVO.shopkeeper_AreaId = shopkeeper_AreaId
        shopkeeperVO.shopkeeperAddress = shopkeeperAddress
        shopkeeperVO.shopkeeperContact = shopkeeperContact
        shopkeeperVO.shopkeeper_LoginId = loginVO.loginId
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        shopkeeperDAO.insertShopkeeper(shopkeeperVO)

        server.quit()

        return render_template("admin/login.html")

    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/loadDashboard')
def shopkeeperLoadDashboard():
    try:
        if adminLoginSession() == 'shopkeeper':
            shopkeeperDAO = ShopkeeperDAO()
            shopkeeperVOList = shopkeeperDAO.viewShopkeeperIndex()

        return render_template('shopkeeper/index.html', shopkeeperVOList=shopkeeperVOList)
    except Exception as ex:
        print(ex)


@app.route('/admin/viewShopkeeper')
def adminViewShopkeeper():
    try:
        if adminLoginSession() == 'admin':

            shopkeeperDAO = ShopkeeperDAO()
            shopkeeperVOList = shopkeeperDAO.viewShopkeeper()

            return render_template('admin/viewShopkeeper.html', shopkeeperVOList=shopkeeperVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/manageShopkeeper')
def adminManageShopkeeper():
    try:
        if adminLoginSession() == 'admin':

            loginId = request.args.get('loginId')

            loginVO = LoginVO()
            shopkeeperDAO = ShopkeeperDAO()

            loginVOList = shopkeeperDAO.validateLogin(loginId)

            loginDictList = [i.as_dict() for i in loginVOList]

            if loginDictList[0]['loginStatus'] == "active":

                loginStatus = "inactive"

                loginVO.loginId = loginId
                loginVO.loginStatus = loginStatus

                shopkeeperDAO.manageShopkeeper(loginVO)

                return redirect(url_for("adminViewShopkeeper"))

            elif loginDictList[0]['loginStatus'] == "inactive":

                loginStatus = "active"

                loginVO.loginId = loginId
                loginVO.loginStatus = loginStatus

                shopkeeperDAO.manageShopkeeper(loginVO)

                return redirect(url_for("adminViewShopkeeper"))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

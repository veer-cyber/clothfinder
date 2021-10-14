from flask import request, render_template, redirect, url_for, session

from snap_shopusingai.project import app
from snap_shopusingai.project.com.dao.LoginDAO import LoginDAO
from snap_shopusingai.project.com.vo.LoginVO import LoginVO


@app.route('/', methods=['GET'])
def adminLoadLogin():
    try:
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST', 'GET'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        # loginVO.loginStatus = "active"

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)
        print("333333333")
        print(lenLoginDictList)

        if lenLoginDictList == 0:

            msg = 'Username Or Password is Incorrect !'

            return render_template('admin/login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == "inactive":

            msg = 'You are Temporarily Blocked by Admin'

            return render_template('admin/login.html', error=msg)

        else:

            for row1 in loginDictList:

                loginId = row1['loginId']
                print(loginId)
                print("VARDHILVARDHILVARDHIL")

                loginUsername = row1['loginUsername']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))

                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))

                elif loginRole == 'shopkeeper':
                    return redirect(url_for('shopkeeperLoadDashboard'))

    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard')
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/index.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':

                return 'admin'

            elif session['session_loginRole'] == 'user':

                return 'user'

            elif session['session_loginRole'] == 'shopkeeper':
                return 'shopkeeper'

            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

        else:

            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

            return False

    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:

        session.clear()
        return redirect('/')
    except Exception as ex:
        print(ex)

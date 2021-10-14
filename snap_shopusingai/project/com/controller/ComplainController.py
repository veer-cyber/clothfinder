import os

from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename

from snap_shopusingai.project import app
from snap_shopusingai.project.com.dao.ComplainDAO import ComplainDAO
from snap_shopusingai.project.com.vo.ComplainVO import ComplainVO

UPLOAD_FOLDER = 'snap_shopusingai/project/static/adminResources/shopkeepercomplain/'
UPLOAD_FOLDER_REPLY = 'snap_shopusingai/project/static/adminResources/shopkeeperreply/'
UPLOAD_FOLDER_USER_COMPLAIN = 'project/static/adminResources/usercomplain/'
UPLOAD_FOLDER_USER_REPLY = 'project/static/adminResources/userreply/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_REPLY'] = UPLOAD_FOLDER_REPLY
app.config['UPLOAD_FOLDER_USER_COMPLAIN'] = UPLOAD_FOLDER_USER_COMPLAIN
app.config['UPLOAD_FOLDER_USER_REPLY'] = UPLOAD_FOLDER_USER_REPLY

from datetime import datetime
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession


# ------------------------------------ ADMIN -------------------------------------------------------


@app.route('/admin/viewComplain', methods=['GET'])
def adminViewComplain():
    try:
        if adminLoginSession() == "admin":
            complainDAO = ComplainDAO()
            complainVOList = complainDAO.adminviewComplain()

            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReply():
    try:
        if adminLoginSession() == "admin":

            complainId = request.args.get('complainId')
            print(complainId)

            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST', 'GET'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == "admin":

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.form['complainId']
            print(complainId)
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']
            file = request.files['file']
            replyFileName = secure_filename(file.filename)
            print(replyFileName)

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER_REPLY'])
            print(replyFilePath)
            complainStatus = "Replied"

            now = datetime.now()
            replyDate = now.strftime("%d/%m/%Y")
            replyTime = now.strftime("%H:%M:%S")
            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO.complainId = complainId
            complainVO.complainStatus = complainStatus
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = session['session_loginId']
            complainDAO.insertComplainReply(complainVO)

            return redirect(url_for('adminViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ------------------------------------ SHOPKEEPER ----------------------------------------------------------


@app.route('/shopkeeper/loadComplain', methods=['GET'])
def shopkeeperLoadComplain():
    try:
        if adminLoginSession() == "shopkeeper":
            return render_template('shopkeeper/addComplain.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/insertComplain', methods=['POST', 'GET'])
def shopkeeperInsertComplain():
    try:
        if adminLoginSession() == "shopkeeper":

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']
            file = request.files['file']
            print(file)
            complainFileName = secure_filename(file.filename)
            print(complainFileName)
            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(complainFilePath)
            now = datetime.now()
            complainDate = now.strftime("%d/%m/%Y")
            complainTime = now.strftime("%H:%M:%S")
            print(complainDate)
            print(complainTime)
            file.save(os.path.join(complainFilePath, complainFileName))
            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription

            complainVO.complainFileName = complainFileName

            complainVO.complainFilePath = complainFilePath.replace("project", "..")

            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime

            complainVO.complainStatus = 'Pending'

            complainVO.complainFrom_LoginId = session['session_loginId']
            complainDAO.insertComplain(complainVO)
            return redirect(url_for('shopkeeperViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/viewComplain', methods=['GET'])
def shopkeeperViewComplain():
    try:
        if adminLoginSession() == "shopkeeper":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainVOList = complainDAO.viewComplain(complainVO)

            return render_template('shopkeeper/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/viewComplainReply', methods=['GET'])
def shopkeeperViewComplainReply():
    try:
        if adminLoginSession() == "shopkeeper":

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId

            complainVOList = complainDAO.viewComplainReply(complainVO)

            return render_template('shopkeeper/viewComplainReply.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/deleteComplain', methods=['GET'])
def shopkeeperDeleteComplain():
    try:
        if adminLoginSession() == "shopkeeper":
            complainDAO = ComplainDAO()

            complainVO = ComplainVO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            complainList = complainDAO.deleteComplain(complainVO)
            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath

            print(complainFileName)

            replyFileName = complainList.replyFileName
            replyFilePath = complainList.replyFilePath

            path = complainFilePath.replace("..", "project") + complainFileName
            os.remove(path)

            if complainList.complainStatus == 'Replied':
                path = replyFilePath.replace("..", "project") + replyFileName
                os.remove(path)

            return redirect(url_for('shopkeeperViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/viewUserComplain', methods=['GET'])
def shopkeeperViewUserComplain():
    try:
        if adminLoginSession() == "shopkeeper":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainStatus = "Pending"

            complainVO.complainStatus = complainStatus
            complainVOList = complainDAO.viewUserComplain(complainVO)
            print(complainVOList)

            return render_template('shopkeeper/viewUserComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/loadComplainReply', methods=['GET'])
def shopkeeperLoadComplainReply():
    try:
        if adminLoginSession() == "shopkeeper":

            complainId = request.args.get('complainId')
            print(complainId)

            return render_template('shopkeeper/addComplainReply.html', complainId=complainId)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/insertComplainReply', methods=['POST', 'GET'])
def shopkeeperInsertComplainReply():
    try:
        if adminLoginSession() == "shopkeeper":

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.form['complainId']

            complainStatus = "Replied"

            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            file = request.files['file']

            replyFileName = secure_filename(file.filename)
            print(replyFileName)

            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER_USER_REPLY'])
            print(replyFilePath)

            now = datetime.now()
            replyDate = now.strftime("%d/%m/%Y")
            replyTime = now.strftime("%H:%M:%S")
            file.save(os.path.join(replyFilePath, replyFileName))
            complainVO.complainId = complainId
            complainVO.complainStatus = complainStatus
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = session['session_loginId']

            complainDAO.insertComplainReply(complainVO)

            return redirect(url_for('shopkeeperViewUserComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# -------------------------------------- USER ---------------------------------------------------------------


@app.route('/user/loadComplain', methods=['GET'])
def userLoadComplain():
    try:
        if adminLoginSession() == "user":
            return render_template('user/addComplain.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST', 'GET'])
def userInsertComplain():
    try:
        if adminLoginSession() == "user":

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']
            file = request.files['file']
            print(file)
            complainFileName = secure_filename(file.filename)
            print(complainFileName)
            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER_USER_COMPLAIN'])
            print(complainFilePath)
            now = datetime.now()
            complainDate = now.strftime("%d/%m/%Y")
            complainTime = now.strftime("%H:%M:%S")
            print(complainDate)
            print(complainTime)
            file.save(os.path.join(complainFilePath, complainFileName))
            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription

            complainVO.complainFileName = complainFileName

            complainVO.complainFilePath = complainFilePath.replace("project", "..")

            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime

            complainVO.complainStatus = 'Pending'

            complainVO.complainFrom_LoginId = session['session_loginId']
            complainDAO.insertComplain(complainVO)
            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain', methods=['GET'])
def userViewComplain():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainVO.complainFrom_LoginId = session['session_loginId']

            complainVOList = complainDAO.viewComplain(complainVO)

            return render_template('user/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply', methods=['GET'])
def userViewComplainReply():
    try:
        if adminLoginSession() == "user":

            complainDAO = ComplainDAO()

            complainVO = ComplainVO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainVOList = complainDAO.viewComplainReply(complainVO)

            return render_template('user/viewComplainReply.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()

            complainVO = ComplainVO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId

            complainList = complainDAO.deleteComplain(complainVO)
            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath

            path = complainFilePath.replace("..", "project") + complainFileName
            os.remove(path)

            if complainList.complainStatus == 'Replied':
                replyFileName = complainList.replyFileName
                replyFilePath = complainList.replyFilePath

                path = replyFilePath.replace("..", "project") + replyFileName
                os.remove(path)

            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

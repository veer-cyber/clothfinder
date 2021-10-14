from datetime import datetime

from flask import request, render_template, redirect, url_for, session

from snap_shopusingai.project import app
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from snap_shopusingai.project.com.dao.FeedbackDAO import FeedbackDAO
from snap_shopusingai.project.com.vo.FeedbackVO import FeedbackVO


# ------------------------------------ ADMIN ----------------------------------------------------


@app.route('/admin/viewFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        if adminLoginSession() == "admin":
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.adminviewFeedback()

            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewFeedbackReview')
def adminViewFeedbackReview():
    try:
        if adminLoginSession() == "admin":
            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            print(feedbackId)

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.viewFeedbackReview(feedbackVO)

            return redirect(url_for('adminViewFeedback'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# -------------------------------------- SHOPKEEPER --------------------------------------------------------


@app.route('/shopkeeper/loadFeedback', methods=['GET'])
def shopkeeperLoadFeedback():
    try:
        if adminLoginSession() == "shopkeeper":
            return render_template('shopkeeper/addFeedback.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/insertFeedback', methods=['POST', 'GET'])
def shopkeeperInsertFeedback():
    try:
        if adminLoginSession() == "shopkeeper":

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            now = datetime.now()
            feedbackDate = now.strftime("%d/%m/%Y")
            feedbackTime = now.strftime("%H:%M:%S")
            print(feedbackDate)
            print(feedbackTime)
            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']
            feedbackDAO.insertFeedback(feedbackVO)
            return redirect(url_for('shopkeeperViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/viewFeedback', methods=['GET'])
def shopkeeperViewFeedback():
    try:
        if adminLoginSession() == "shopkeeper":
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)

            return render_template('shopkeeper/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/deleteFeedback', methods=['GET'])
def shopkeeperDeleteFeedback():
    try:
        if adminLoginSession() == "shopkeeper":
            feedbackDAO = FeedbackDAO()

            feedbackId = request.args.get('feedbackId')

            feedbackDAO.deleteFeedback(feedbackId)

            return redirect(url_for('shopkeeperViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/viewUserFeedback', methods=['GET'])
def shopkeeperViewUserFeedback():
    try:
        if adminLoginSession() == "shopkeeper":
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.shopkeeperviewFeedback()

            return render_template('shopkeeper/viewUserFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/viewUserFeedbackReview')
def shopkeeperViewUserFeedbackReview():
    try:
        if adminLoginSession() == "shopkeeper":
            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            print(feedbackId)

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.viewFeedbackReview(feedbackVO)

            return redirect(url_for('shopkeeperViewUserFeedback'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ----------------------------------------- USER -------------------------------------------------------


@app.route('/user/loadFeedback', methods=['GET'])
def userLoadFeedback():
    try:
        if adminLoginSession() == "user":
            return render_template('user/addFeedback.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST', 'GET'])
def userInsertFeedback():
    try:
        if adminLoginSession() == "user":

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            now = datetime.now()
            feedbackDate = now.strftime("%d/%m/%Y")
            feedbackTime = now.strftime("%H:%M:%S")
            print(feedbackDate)
            print(feedbackTime)

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewFeedback', methods=['GET'])
def userViewFeedback():
    try:
        if adminLoginSession() == "user":
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)

            return render_template('user/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback', methods=['GET'])
def userDeleteFeedback():
    try:
        if adminLoginSession() == "user":
            feedbackDAO = FeedbackDAO()

            feedbackId = request.args.get('feedbackId')

            feedbackDAO.deleteFeedback(feedbackId)

            return redirect(url_for('userViewFeedback'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

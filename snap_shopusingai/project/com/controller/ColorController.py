from flask import request, render_template, redirect, url_for

from snap_shopusingai.project import app
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from snap_shopusingai.project.com.dao.ColorDAO import ColorDAO
from snap_shopusingai.project.com.vo.ColorVO import ColorVO


@app.route('/admin/loadColor', methods=['GET'])
def adminLoadColor():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addColor.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertColor', methods=['POST', 'GET'])
def adminInsertColor():
    try:
        if adminLoginSession() == 'admin':
            colorName = request.form['colorName']
            colorHexcode = request.form['colorHexcode']

            colorVO = ColorVO()
            colorDAO = ColorDAO()

            colorVO.colorName = colorName
            colorVO.colorHexcode = colorHexcode

            colorDAO.insertColor(colorVO)
            return redirect(url_for('adminViewColor'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewColor', methods=['GET'])
def adminViewColor():
    try:
        if adminLoginSession() == 'admin':

            colorDAO = ColorDAO()
            colorVOList = colorDAO.viewColor()
            print("__________________", colorVOList)

            return render_template('admin/viewColor.html', colorVOList=colorVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteColor', methods=['GET'])
def adminDeleteColor():
    try:
        if adminLoginSession() == 'admin':
            colorVO = ColorVO()
            colorDAO = ColorDAO()

            colorId = request.args.get('colorId')

            colorVO.colorId = colorId

            colorDAO.deleteColor(colorVO)

            return redirect(url_for('adminViewColor'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editColor', methods=['GET'])
def adminEditColor():
    try:
        if adminLoginSession() == 'admin':
            colorVO = ColorVO()

            colorDAO = ColorDAO()

            colorId = request.args.get('colorId')

            colorVO.colorId = colorId

            colorVOList = colorDAO.editColor(colorVO)

            print("=======categoryVOList=======", colorVOList)

            print("=======type of categoryVOList=======", type(colorVOList))

            return render_template('admin/editColor.html', colorVOList=colorVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateColor', methods=['POST', 'GET'])
def adminUpdateColor():
    try:
        if adminLoginSession() == 'admin':
            colorId = request.form['colorId']
            colorName = request.form['colorName']
            colorHexcode = request.form['colorHexcode']

            colorVO = ColorVO()
            colorDAO = ColorDAO()

            colorVO.colorId = colorId
            colorVO.colorName = colorName
            colorVO.colorHexcode = colorHexcode

            colorDAO.updateColor(colorVO)

            return redirect(url_for('adminViewColor'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

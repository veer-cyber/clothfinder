from flask import request, render_template, redirect, url_for

from snap_shopusingai.project import app
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from snap_shopusingai.project.com.dao.CategoryDAO import CategoryDAO
from snap_shopusingai.project.com.vo.CategoryVO import CategoryVO


@app.route('/admin/loadCategory', methods=['GET'])
def adminLoadCategory():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addCategory.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertCategory', methods=['POST', 'GET'])
def adminInsertCategory():
    try:
        if adminLoginSession() == 'admin':

            categoryName = request.form['categoryName']
            categoryDescription = request.form['categoryDescription']

            categoryVO = CategoryVO()
            categoryDAO = CategoryDAO()

            categoryVO.categoryName = categoryName
            categoryVO.categoryDescription = categoryDescription

            categoryDAO.insertCategory(categoryVO)

            return redirect(url_for('adminViewCategory'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewCategory', methods=['GET'])
def adminViewCategory():
    try:
        if adminLoginSession() == 'admin':

            categoryDAO = CategoryDAO()
            categoryVOList = categoryDAO.viewCategory()
            print("__________________", categoryVOList)

            return render_template('admin/viewCategory.html', categoryVOList=categoryVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCategory', methods=['GET'])
def adminDeleteCategory():
    try:
        if adminLoginSession() == 'admin':
            categoryVO = CategoryVO()

            categoryDAO = CategoryDAO()

            categoryId = request.args.get('categoryId')

            categoryVO.categoryId = categoryId

            categoryDAO.deleteCategory(categoryVO)

            return redirect(url_for('adminViewCategory'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editCategory', methods=['GET'])
def adminEditCategory():
    try:
        if adminLoginSession() == 'admin':
            categoryVO = CategoryVO()

            categoryDAO = CategoryDAO()

            categoryId = request.args.get('categoryId')

            categoryVO.categoryId = categoryId

            categoryVOList = categoryDAO.editCategory(categoryVO)

            print("=======categoryVOList=======", categoryVOList)

            print("=======type of categoryVOList=======", type(categoryVOList))

            return render_template('admin/editCategory.html', categoryVOList=categoryVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateCategory', methods=['POST', 'GET'])
def adminUpdateCategory():
    try:
        if adminLoginSession() == 'admin':

            categoryId = request.form['categoryId']
            categoryName = request.form['categoryName']
            categoryDescription = request.form['categoryDescription']

            categoryVO = CategoryVO()
            categoryDAO = CategoryDAO()

            categoryVO.categoryId = categoryId
            categoryVO.categoryName = categoryName
            categoryVO.categoryDescription = categoryDescription

            categoryDAO.updateCategory(categoryVO)

            return redirect(url_for('adminViewCategory'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

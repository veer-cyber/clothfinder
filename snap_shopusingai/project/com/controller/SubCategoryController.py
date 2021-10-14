from flask import request, render_template, redirect, url_for

from snap_shopusingai.project import app
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from snap_shopusingai.project.com.dao.CategoryDAO import CategoryDAO
from snap_shopusingai.project.com.dao.SubCategoryDAO import SubCategoryDAO
from snap_shopusingai.project.com.vo.SubCategoryVO import SubCategoryVO


@app.route('/admin/loadSubCategory', methods=['GET'])
def adminLoadSubCategory():
    try:
        if adminLoginSession() == 'admin':
            categoryDAO = CategoryDAO()
            categoryVOList = categoryDAO.viewCategory()
            return render_template('admin/addSubCategory.html', categoryVOList=categoryVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertSubCategory', methods=['POST', 'GET'])
def adminInsertSubCategory():
    try:
        if adminLoginSession() == 'admin':
            subCategoryName = request.form['subCategoryName']
            subCategoryDescription = request.form['subCategoryDescription']
            subCategory_CategoryId = request.form['subCategory_CategoryId']

            subCategoryVO = SubCategoryVO()
            subCategoryDAO = SubCategoryDAO()

            subCategoryVO.subCategoryName = subCategoryName
            subCategoryVO.subCategoryDescription = subCategoryDescription
            subCategoryVO.subCategory_CategoryId = subCategory_CategoryId

            subCategoryDAO.insertSubCategory(subCategoryVO)
            return redirect(url_for('adminViewSubCategory'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewSubCategory', methods=['GET'])
def adminViewSubCategory():
    try:
        if adminLoginSession() == 'admin':

            subCategoryDAO = SubCategoryDAO()

            subCategoryVOList = subCategoryDAO.viewSubCategory()
            print("__________________", subCategoryVOList)
            return render_template('admin/viewSubCategory.html', subCategoryVOList=subCategoryVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteSubCategory', methods=['GET'])
def adminDeleteSubCategory():
    try:
        if adminLoginSession() == 'admin':

            subCategoryDAO = SubCategoryDAO()

            subCategoryId = request.args.get('subCategoryId')

            SubCategoryVO.categoryId = subCategoryId

            subCategoryDAO.deleteSubCategory(subCategoryId)

            return redirect(url_for('adminViewSubCategory'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/editSubCategory', methods=['GET'])
def adminEditSubCategory():
    try:
        if adminLoginSession() == 'admin':

            subCategoryVO = SubCategoryVO()

            subCategoryDAO = SubCategoryDAO()

            categoryDAO = CategoryDAO()
            subCategoryId = request.args.get('subCategoryId')

            subCategoryVO.subCategoryId = subCategoryId

            subCategoryVOList = subCategoryDAO.editSubCategory(subCategoryVO)

            categoryVOList = categoryDAO.viewCategory()

            print("=======subCategoryVOList=======", subCategoryVOList)

            print("=======type of categoryVOList=======", type(subCategoryVOList))

            return render_template('admin/editSubCategory.html', categoryVOList=categoryVOList,
                                   subCategoryVOList=subCategoryVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateSubCategory', methods=['POST', 'GET'])
def adminUpdateSubCategory():
    try:
        if adminLoginSession() == 'admin':
            subCategoryName = request.form['subCategoryName']
            subCategoryDescription = request.form['subCategoryDescription']
            subCategory_CategoryId = request.form['subCategory_CategoryId']
            subCategoryId = request.form['subCategoryId']

            subCategoryVO = SubCategoryVO()
            subCategoryDAO = SubCategoryDAO()

            subCategoryVO.subCategoryId = subCategoryId
            subCategoryVO.subCategoryName = subCategoryName
            subCategoryVO.subCategoryDescription = subCategoryDescription
            subCategoryVO.subCategory_CategoryId = subCategory_CategoryId

            subCategoryDAO.updateSubCategory(subCategoryVO)

            return redirect(url_for('adminViewSubCategory'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

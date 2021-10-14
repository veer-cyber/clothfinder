import os

from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename

from snap_shopusingai.project import app
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from snap_shopusingai.project.com.dao.CategoryDAO import CategoryDAO
from snap_shopusingai.project.com.dao.ProductDAO import ProductDAO
from snap_shopusingai.project.com.dao.SubCategoryDAO import SubCategoryDAO
from snap_shopusingai.project.com.vo.ProductVO import ProductVO

UPLOAD_FOLDER = 'project/static/adminResources/shopkeeperproduct/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/shopkeeper/loadProduct', methods=['GET'])
def shopkeeperLoadProduct():
    try:
        if adminLoginSession() == 'shopkeeper':
            categoryDAO = CategoryDAO()
            categoryVOList = categoryDAO.viewCategory()

            subCategoryDAO = SubCategoryDAO()
            subCategoryVOList = subCategoryDAO.viewSubCategory()

            return render_template('shopkeeper/addProduct.html', categoryVOList=categoryVOList,
                                   subCategoryVOList=subCategoryVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/insertProduct', methods=['POST', 'GET'])
def shopkeeperInsertProduct():
    try:
        if adminLoginSession() == 'shopkeeper':

            productName = request.form['productName']
            productDescription = request.form['productDescription']
            productPrice = request.form['productPrice']
            productColorName = request.form['productColorName']
            product_CategoryId = request.form['product_CategoryId']
            product_SubCategoryId = request.form['product_SubCategoryId']
            size = request.form.getlist('productSize')
            productSize = "-".join(size)

            file = request.files['file']

            productFileName = secure_filename(file.filename)
            productFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(productFilePath, productFileName))

            productVO = ProductVO()
            productDAO = ProductDAO()

            print("VEERVEERVEERVEERVEERVEER1")
            print(session['session_loginId'])
            productVO.productName = productName
            productVO.productDescription = productDescription
            productVO.productPrice = productPrice
            productVO.productColorName = productColorName
            productVO.product_CategoryId = product_CategoryId
            productVO.product_SubCategoryId = product_SubCategoryId
            productVO.productFileName = productFileName
            productVO.productFilePath = productFilePath.replace("project", "..")
            productVO.productSize = productSize
            print("HIHIHIHIHI")
            productVO.product_LoginId = session['session_loginId']

            print("VEERVEERVEERVEERVEERVEER2")
            productDAO.insertProduct(productVO)
            print("VEERVEERVEERVEERVEERVEER3")
            return redirect(url_for('shopkeeperViewProduct'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/viewProduct', methods=['GET'])
def shopkeeperViewProduct():
    try:
        if adminLoginSession() == 'shopkeeper':

            productDAO = ProductDAO()
            productVOList = productDAO.viewProduct()
            print("__________________", productVOList)
            return render_template('shopkeeper/viewProduct.html', productVOList=productVOList)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/deleteProduct', methods=['GET'])
def shopkeeperDeleteProduct():
    try:
        if adminLoginSession() == 'shopkeeper':

            productDAO = ProductDAO()
            productVO = ProductVO()
            productId = request.args.get('productId')
            productVO.productId = productId
            productList = productDAO.deleteProduct(productId)

            productFileName = productList.productFileName
            productFilePath = productList.productFilePath
            path = productFilePath.replace("..", "project") + productFileName
            os.remove(path)

            return redirect(url_for('shopkeeperViewProduct'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/editProduct', methods=['GET'])
def shopkeeperEditProduct():
    try:
        if adminLoginSession() == 'shopkeeper':

            productVO = ProductVO()

            productDAO = ProductDAO()

            categoryDAO = CategoryDAO()

            subCategoryDAO = SubCategoryDAO()

            productId = request.args.get('productId')

            productVO.productId = productId

            productVOList = productDAO.editProduct(productVO)

            categoryVOList = categoryDAO.viewCategory()

            subCategoryVOList = subCategoryDAO.viewSubCategory()

            print("=======subCategoryVOList=======", productVOList)

            print("=======type of categoryVOList=======", type(productVOList))

            return render_template('shopkeeper/editProduct.html', categoryVOList=categoryVOList,
                                   subCategoryVOList=subCategoryVOList,
                                   productVOList=productVOList)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/shopkeeper/updateProduct', methods=['POST', 'GET'])
def shopkeeperUpdateProduct():
    try:
        if adminLoginSession() == 'shopkeeper':

            productId = request.form['productId']
            productName = request.form['productName']
            productDescription = request.form['productDescription']
            productPrice = request.form['productPrice']
            productColorName = request.form['productColorName']
            product_CategoryId = request.form['product_CategoryId']
            product_SubCategoryId = request.form['product_SubCategoryId']
            size = request.form.getlist('productSize')
            productSize = "-".join(size)

            productVO = ProductVO()
            productDAO = ProductDAO()

            productVO.productId = productId
            productVO.productName = productName
            productVO.productDescription = productDescription
            productVO.productPrice = productPrice
            productVO.productColorName = productColorName
            productVO.product_CategoryId = product_CategoryId
            productVO.product_SubCategoryId = product_SubCategoryId
            productVO.productSize = productSize

            productDAO.updateProduct(productVO)

            return redirect(url_for('shopkeeperViewProduct'))

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

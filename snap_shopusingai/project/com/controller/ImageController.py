import os
from datetime import datetime

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from snap_shopusingai.project import app
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from snap_shopusingai.project.com.dao.ImageDAO import ImageDAO
from snap_shopusingai.project.com.vo.ImageVO import ImageVO

UPLOAD_IMAGE_FOLDER = 'project/static/adminResources/userImage/'
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER


@app.route('/user/loadImage', methods=['GET'])
def userLoadImage():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addImage.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertImage', methods=['POST', 'GET'])
def userInsertImage():
    try:
        if adminLoginSession() == 'user':
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            imageVO = ImageVO()
            imageDAO = ImageDAO()

            uploadDate = str(datetime.now().date())
            uploadTime = datetime.now().strftime("%H:%M:%S")
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            file = request.files['file']

            imageFileName = secure_filename(file.filename)

            print("############################################################")
            imageFilePath = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'])
            print("111111111111111111111111111111111111111111111111111111111111")
            file.save(os.path.join(imageFilePath, imageFileName))

            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            imageVO.imageFileName = imageFileName
            imageVO.imageFilePath = imageFilePath.replace("project", "..")
            imageVO.imageUploadDate = uploadDate
            imageVO.imageUploadTime = uploadTime

            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            imageDAO.insertImage(imageVO)

            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&11")
            return redirect(url_for('userViewImage'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewImage', methods=['GET'])
def userViewImage():
    try:
        if adminLoginSession() == 'user':

            imageDAO = ImageDAO()
            imageVOList = imageDAO.viewImage()
            print("_____________", imageVOList)
            return render_template('user/viewImage.html', imageVOList=imageVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteImage', methods=['GET'])
def userDeleteImage():
    try:
        if adminLoginSession() == 'user':

            imageVO = ImageVO()
            imageDAO = ImageDAO()
            imageId = request.args.get('imageId')

            imageVO.imageId = imageId

            imageList = imageDAO.deleteImage(imageVO)

            imageFileName = imageList.imageFileName
            imageFilePath = imageList.imageFilePath

            path = imageFilePath.replace("..", "project") + imageFileName

            os.remove(path)

            return redirect(url_for('userViewImage'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)

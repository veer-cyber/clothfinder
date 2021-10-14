import os
import glob
from datetime import datetime

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from snap_shopusingai.project import app
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from snap_shopusingai.project.com.dao.ImageDAO import ImageDAO
from snap_shopusingai.project.com.vo.ImageVO import ImageVO
from snap_shopusingai.project.com.dao.ProductDAO import ProductDAO
from snap_shopusingai.project.com.vo.ProductVO import ProductVO

UPLOAD_IMAGE_FOLDER = 'project/static/adminResources/userImage/'
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER


@app.route('/admin/viewImage')
def adminViewImage():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/viewImage.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewSuggestion')
def adminViewSuggestion():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/viewSuggestion.html')
        elif adminLoginSession() == 'user':
            return render_template('user/viewSuggestion.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)









from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    print(str(m) + "                 " + str(s))
    return s















@app.route('/user/viewSuggestion', methods = ['POST'])
def userViewSuggestion():
    try:
        print("I am in view suggestion")
        dataCheck = "Prog"
        print(dataCheck)
        if adminLoginSession() == 'user' and 'pari' == request.form['dataCheck']:
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
            count = 0
            count1 = 0
            filenameValue = ""
            for filename in glob.glob(r"project\static\adminResources\shopkeeperproduct\*.jpg"):
                print(filename)
                # load the images -- the original, the original + contrast,
                # and the original + photoshop
                original = cv2.imread(os.path.join(imageFilePath, imageFileName))
                contrast = cv2.imread(filename)

                # convert the images to grayscale
                original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
                contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

                value = compare_images(original, contrast, "Original vs. Original")
                if value > count and value > 0.50:
                    count = value
                    filenameValue = filename
                    print("FINISHFINISHFINISH")
                    print(str(count) + "                    " + filenameValue)

            print("OUTOUTOUTOUTOUT")
            print(str(count) + "                    " + str(filenameValue))
            filenameValue = str(filenameValue).replace("project\\static\\adminResources\\shopkeeperproduct\\","")
            print(filenameValue)

            productDAO = ProductDAO()
            productVO = ProductVO()
            productVO.productFileName = filenameValue
            productVOList = productDAO.getSpecificProduct(productVO)
            print("DONEDOMN")
            print(productVOList)

            return render_template('user/viewSuggestion.html', productVOList=productVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

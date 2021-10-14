import os
from datetime import datetime

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from snap_shopusingai.project import app
from snap_shopusingai.project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from snap_shopusingai.project.com.dao.DatasetDAO import DatasetDAO
from snap_shopusingai.project.com.vo.DatasetVO import DatasetVO

UPLOAD_FOLDER = 'project/static/adminResources/dataset/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/loadDataset', methods=['GET'])
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addDataset.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST', 'GET'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()
            dataDAO = DatasetDAO()

            uploadDate = str(datetime.now().date())
            uploadTime = datetime.now().strftime("%H:%M:%S")

            file = request.files['file']

            datasetFileName = secure_filename(file.filename)

            datasetFilePath = os.path.join(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(datasetFilePath, datasetFileName))

            datasetVO.datasetFileName = datasetFileName
            datasetVO.datasetFilePath = datasetFilePath.replace("project", "..")
            datasetVO.datasetUploadDate = uploadDate
            datasetVO.datasetUploadTime = uploadTime

            dataDAO.insertDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset', methods=['GET'])
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            print("_____________", datasetVOList)
            return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()
            datasetId = request.args.get('datasetId')

            datasetVO.datasetId = datasetId

            datasetList = datasetDAO.deleteDataset(datasetVO)

            datasetFileName = datasetList.datasetFileName
            datasetFilePath = datasetList.datasetFilePath

            path = datasetFilePath.replace("..", "project") + datasetFileName

            os.remove(path)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

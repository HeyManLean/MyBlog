import os

from flask_restful import Resource
from flask_login import login_required
from flask import request

from app.utils.file import cal_md5
from config import Config


class FileResource(Resource):
    # @login_required
    def post(self):
        image_file = request.files['image']
        file_md5 = cal_md5(image_file.read())
        file_ext = os.path.splitext(image_file.filename)[-1]
        filename = file_md5 + file_ext
        image_file.seek(0, 0)
        image_file.save(
            os.path.join(Config.DOWNLOAD_DIR, filename)
        )
        file_url = 'http://{0}/files/{1}'.format(request.host, filename)
        data = dict(
            code=200,
            message='ok',
            file_url=file_url
        )
        return data

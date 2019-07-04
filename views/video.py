import uuid

from flask import Blueprint, jsonify
from flask import request


blue = Blueprint('video_blue', __name__)


@blue.route('/upload_video/', methods=("POST", ))
def upload_video():
    # 上传视频的文件字段名 video
    video_file = request.files.get('video')

    filename = uuid.uuid4().hex + ".mp4"

    video_file.save('/var/flvs/%s' % filename)

    return jsonify({
        'url': "rtmp://121.199.63.71/vod/%s" % filename
    })
from flask import request, jsonify, Blueprint

from apps.paint import handler as paintHandler
from apps.paint import logic as paintLogic

from apps.utils import ResponseWrapper, BusinessException, BUSINESS_FAIL

apps = Blueprint("apps", __name__)


@apps.route('/ping', methods=['GET', 'POST'])
def index():
    return "pong"


@apps.route('/generate', methods=['POST'])
def generate():
    try:
        # app_id = int(request.form.get('appid'))
        # type_ = int(request.form.get('type'))
        # prompts = request.form.get('prompts')
        # data = request.files['image'].read()
        app_id = int(request.json.get('appid'))
        type_ = int(request.json.get('type'))
        prompts = request.json.get('prompts')

        if app_id == 0:
            # response_data = paintHandler.handle_request(type_, prompts, data)
            response_data = paintHandler.handle_request(type_, prompts)
        else:
            raise BusinessException(message="应用不存在")
        
        return jsonify(ResponseWrapper.success(data=response_data))
    except BusinessException as be:
        return jsonify(ResponseWrapper.fail(code=be.code, message=be.message))
    except Exception as e:
        return jsonify(ResponseWrapper.fail(code=BUSINESS_FAIL, message=str(e)))

@apps.route('/paint/save', methods=['POST'])
def paintSave():
    try:
        username = request.json.get('username')
        data = request.json.get('data')
        paintLogic.save(username, data)
        return jsonify(ResponseWrapper.success())
    except BusinessException as be:
        return jsonify(ResponseWrapper.fail(code=be.code, message=be.message))
    except Exception as e:
        return jsonify(ResponseWrapper.fail(code=BUSINESS_FAIL, message=str(e)))
    
@apps.route('/paint/start', methods=['POST'])
def paintStart():
    try:
        username = request.json.get('username')
        response_data = paintLogic.start(username)
        return jsonify(ResponseWrapper.success(data=response_data))
    except BusinessException as be:
        return jsonify(ResponseWrapper.fail(code=be.code, message=be.message))
    except Exception as e:
        return jsonify(ResponseWrapper.fail(code=BUSINESS_FAIL, message=str(e)))
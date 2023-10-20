SUCCESS = 0
BUSINESS_FAIL = 1


class ResponseWrapper:
    @staticmethod
    def success(data):
        return {
            'success': True,
            'data': data,
            'code': SUCCESS,
            'message': ''
        }

    @staticmethod
    def fail(code, message):
        return {
            'success': False,
            'data': None,
            'code': code,
            'message': message
        }


class BusinessException(Exception):
    def __init__(self, message, code=BUSINESS_FAIL):
        self.code = code
        self.message = message
        super().__init__(self.message)
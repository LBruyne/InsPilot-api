from apps.utils import BusinessException

AGENT_FAIL_CODE = 2


class AgentException(BusinessException):
    def __init__(self, message, code=AGENT_FAIL_CODE):
        super().__init__(code, message)

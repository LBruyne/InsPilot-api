from apps.paint.logic import rapid_divergence_stimulus, deep_divergence_stimulus, convergence_1_stimulus, convergence_2_stimulus
from apps.utils import BusinessException, BUSINESS_FAIL


def handle_request(type_, prompts):
    try:
        if type_ == 0:
            result = rapid_divergence_stimulus(prompts)
        elif type_ == 1:
            result = deep_divergence_stimulus(prompts)
        elif type_ == 2:
            result = convergence_1_stimulus(prompts)
        elif type_ == 3:
            result = convergence_2_stimulus(prompts)
        else:
            raise BusinessException(BUSINESS_FAIL, '无效的任务类型')
        return result

    except BusinessException as be:
        raise be
    except Exception as e:
        raise BusinessException(BUSINESS_FAIL, str(e))

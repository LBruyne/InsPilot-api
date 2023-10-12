from apps.utils import BusinessException, BUSINESS_FAIL


def generate_related_products(task):
    # 设计相关prompts
    return []


def rapid_divergence_stimulus(prompts):
    try:
        task = prompts.get('task')
        if not task:
            raise BusinessException(BUSINESS_FAIL, '设计任务缺失')
        # 根据设计任务生成相关产品
        generated_products = generate_related_products(task)
        #
        return {
            'generatedProducts': generated_products
        }
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e

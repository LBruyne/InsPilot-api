from apps.utils import BusinessException, BUSINESS_FAIL
from apps.paint.creatives import DesignCreative
from agent.gpt import chat
from agent.sd import pool

from settings.prompts import generate_prompts
from settings import rapid_divergence, deep_divergence, convergence_1, convergence_2

from concurrent.futures import ThreadPoolExecutor


def parse_generated(generated_text):
    return generated_text.strip().split('#')


def rapid_divergence_stimulus(prompts):
    try:
        task = prompts.get('task')
        if not task:
            raise BusinessException(BUSINESS_FAIL, '设计任务缺失')
        num = prompts.get('num')
        if not num:
            raise BusinessException(BUSINESS_FAIL, '设计数量缺失')

        # Step 1: 产品
        products = chat(generate_prompts(rapid_divergence.prompt_rapid_divergence_0, input=task, num=num))
        # print(products)

        # Step 2: 场景
        scenes = chat(generate_prompts(rapid_divergence.prompt_rapid_divergence_1, input=products, num=num))
        # print(scenes)

        # Step 3: SD 提示
        sd_prompts = chat(generate_prompts(rapid_divergence.prompt_rapid_divergence_2, input=scenes, num=num))

        # Step 4: 并行生成 SD 图片 images = [] for prompt in parse_generated(sd_prompts): print(prompt) img = text2Image(
        # prompt=generate_prompts(rapid_divergence.sd_positive_0, input=prompt),
        # negative_prompt=rapid_divergence.sd_negative_0, options=rapid_divergence.sd_options_0) images.append(img)
        sd_tasks = []
        for idx, prompt in enumerate(parse_generated(sd_prompts)):
            if prompt == '':
                continue

            task = {'index': idx, 'prompt': generate_prompts(rapid_divergence.sd_positive_0, input=prompt),
                    'negative_prompt': rapid_divergence.sd_negative_0, 'options': rapid_divergence.sd_options_0}
            sd_tasks.append(task)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(pool.text2Image, task) for task in sd_tasks]
            images = [future.result() for future in futures]

        # Step 5: 抽象文本
        abstracts = chat(generate_prompts(rapid_divergence.prompt_rapid_divergence_3, input=products, num=num))
        abstract_texts = parse_generated(abstracts)

        if len(images) != len(abstract_texts):
            raise BusinessException(BUSINESS_FAIL, '生成目标数量不一致')

        result = DesignCreative.array_to_dict(DesignCreative.from_rapid_divergence(images=images, texts=abstract_texts))

        return {
            "count": len(result),
            "result": result
        }
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e


def deep_divergence_stimulus(prompts):
    generate_num = 3
    try:
        texts = prompts.get('designTexts')
        if not texts or not isinstance(texts, list) or len(texts) == 0:
            raise BusinessException(BUSINESS_FAIL, '设计文本缺失')
        scheme_id = prompts.get('schemeId')
        if scheme_id is None:
            raise BusinessException(BUSINESS_FAIL, '关联方案缺失')

        texts = ','.join(texts)
        # Step 1: 产品
        products = chat(generate_prompts(deep_divergence.prompt_deep_divergence_0, input=texts, num=generate_num))
        # print(products)

        # Step 2: 场景
        scenes = chat(generate_prompts(deep_divergence.prompt_deep_divergence_1, input=products, num=generate_num))
        # print(scenes)

        # Step 3: SD 提示
        sd_prompts = chat(generate_prompts(deep_divergence.prompt_deep_divergence_2, input=scenes, num=generate_num))

        # Step 4: 并行生成 SD 图片 images = [] for prompt in parse_generated(sd_prompts): print(prompt) img = text2Image(
        # prompt=generate_prompts(rapid_divergence.sd_positive_0, input=prompt),
        # negative_prompt=rapid_divergence.sd_negative_0, options=rapid_divergence.sd_options_0) images.append(img)
        sd_tasks = []
        for idx, prompt in enumerate(parse_generated(sd_prompts)):
            if prompt == '':
                continue

            task = {'index': idx, 'prompt': generate_prompts(deep_divergence.sd_positive_0, input=prompt),
                    'negative_prompt': deep_divergence.sd_negative_0, 'options': deep_divergence.sd_options_0}
            sd_tasks.append(task)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(pool.text2Image, task) for task in sd_tasks]
            images = [future.result() for future in futures]

        # Step 5: 抽象文本
        abstracts = chat(generate_prompts(deep_divergence.prompt_deep_divergence_3, input=products, num=generate_num))
        abstract_texts = parse_generated(abstracts)

        # Step 6: 具体文本
        concretes = chat(generate_prompts(deep_divergence.prompt_deep_divergence_4, input=products, num=generate_num))
        concrete_texts = parse_generated(concretes)

        if len(images) != len(abstract_texts) or len(abstract_texts) != len(concrete_texts):
            raise BusinessException(BUSINESS_FAIL, '生成目标数量不一致')

        result = DesignCreative.array_to_dict(
            DesignCreative.from_deep_divergence(images=images, a_texts=abstract_texts, c_texts=concrete_texts))

        return {
            "schemeId": scheme_id,
            "count": len(result),
            "result": result
        }
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e


def convergence_1_stimulus(prompts):
    try:
        schemes = prompts.get('schemes')
        if not schemes or not isinstance(schemes, list) or len(schemes) == 0:
            raise BusinessException(BUSINESS_FAIL, '设计方案缺失')

        schemes_design_texts = [",".join(scheme.get('designTexts')) for scheme in schemes]
        schemes_num = 3
        if len(schemes) < schemes_num:
            schemes_num = len(schemes)

        if len(schemes) > schemes_num:
            schemes_design_texts = chat(generate_prompts(convergence_1.prompt_convergence_0, input=schemes_design_texts))
            print(schemes_design_texts)

        # Step 2: 场景
        scenes = chat(generate_prompts(convergence_1.prompt_convergence_1, input=schemes_design_texts, num=schemes_num))
        print(scenes)

        # Step 3: SD 提示
        sd_prompts = chat(generate_prompts(convergence_1.prompt_convergence_2, input=scenes, num=schemes_num))

        # Step 4: 场景图片 images = [] for prompt in parse_generated(sd_prompts): print(prompt) img = text2Image(
        # prompt=generate_prompts(rapid_divergence.sd_positive_0, input=prompt),
        # negative_prompt=rapid_divergence.sd_negative_0, options=rapid_divergence.sd_options_0) images.append(img)
        sd_tasks = []
        for idx, prompt in enumerate(parse_generated(sd_prompts)):
            if prompt == '':
                continue

            task = {'index': idx, 'prompt': generate_prompts(convergence_1.sd_positive_0, input=prompt),
                    'negative_prompt': convergence_1.sd_negative_0, 'options': convergence_1.sd_options_0}
            sd_tasks.append(task)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(pool.text2Image, task) for task in sd_tasks]
            abstract_images = [future.result() for future in futures]

        # Step 5: 具体文本
        concretes = chat(
            generate_prompts(convergence_1.prompt_convergence_3, input=schemes_design_texts, num=schemes_num))
        concrete_texts = parse_generated(concretes)
        print(concrete_texts)

        # Step 5: 产品图提示
        sd_prompts_2 = chat(
            generate_prompts(convergence_1.prompt_convergence_4, input=schemes_design_texts, num=schemes_num))

        # Step 6: 产品图生成
        sd_tasks_2 = []
        for idx, prompt in enumerate(parse_generated(sd_prompts_2)):
            if prompt == '':
                continue

            task = {'index': idx, 'prompt': generate_prompts(convergence_1.sd_positive_1, input=prompt),
                    'negative_prompt': convergence_1.sd_negative_1, 'options': convergence_1.sd_options_1}
            sd_tasks_2.append(task)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(pool.text2Image, task) for task in sd_tasks_2]
            concrete_images = [future.result() for future in futures]

        if len(concrete_images) != len(abstract_images) or len(abstract_images) != len(concrete_texts):
            raise BusinessException(BUSINESS_FAIL, '生成目标数量不一致')

        result = DesignCreative.array_to_dict(
            DesignCreative.from_convergence_0(a_images=abstract_images, c_images=concrete_images,
                                              c_texts=concrete_texts))

        return {
            "result": result
        }
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e


def convergence_2_stimulus(prompts):
    generate_num = 3
    try:
        schemes = prompts.get('selectedSchemes')
        if not schemes or not isinstance(schemes, list) or len(schemes) == 0:
            raise BusinessException(BUSINESS_FAIL, '设计方案缺失')

        schemes_design_texts = [",".join(scheme.get('designTexts')) for scheme in schemes]
        product_generate_num = len(schemes_design_texts) * generate_num

        # Step 1: 场景
        scenes = chat(generate_prompts(convergence_2.prompt_convergence_0, input_num=len(schemes_design_texts), num=generate_num, input=schemes_design_texts))
        print(scenes)

        # Step 2: 场景提示
        sd_prompts = chat(generate_prompts(convergence_2.prompt_convergence_1, input=scenes, num=product_generate_num))

        # Step 3: 场景图片
        sd_tasks = []
        for idx, prompt in enumerate(parse_generated(sd_prompts)):
            if prompt == '':
                continue

            task = {'index': idx, 'prompt': generate_prompts(convergence_2.sd_positive_0, input=prompt),
                    'negative_prompt': convergence_2.sd_negative_0, 'options': convergence_2.sd_options_0}
            sd_tasks.append(task)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(pool.text2Image, task) for task in sd_tasks]
            abstract_images = [future.result() for future in futures]

        # Step 4: 具体文本
        concretes = chat(
            generate_prompts(convergence_2.prompt_convergence_2, input_num=len(schemes_design_texts), num=generate_num, input=schemes_design_texts))
        concrete_texts = parse_generated(concretes)
        print(concrete_texts)

        # Step 5: 产品图提示
        sd_prompts_2 = chat(
            generate_prompts(convergence_2.prompt_convergence_3, input=concretes, num=product_generate_num))

        # Step 6: 产品图生成
        sd_tasks_2 = []
        for idx, prompt in enumerate(parse_generated(sd_prompts_2)):
            if prompt == '':
                continue

            task = {'index': idx, 'prompt': generate_prompts(convergence_2.sd_positive_1, input=prompt),
                    'negative_prompt': convergence_2.sd_negative_1, 'options': convergence_2.sd_options_1}
            sd_tasks_2.append(task)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(pool.text2Image, task) for task in sd_tasks_2]
            concrete_images = [future.result() for future in futures]

        if len(concrete_images) != len(abstract_images) or len(abstract_images) != len(concrete_texts):
            raise BusinessException(BUSINESS_FAIL, '生成目标数量不一致')

        result = DesignCreative.array_to_dict(
            DesignCreative.from_convergence_1(a_images=abstract_images, c_images=concrete_images,
                                              c_texts=concrete_texts))

        return {
            "result": result
        }
    except BusinessException as be:
        raise be
    except Exception as e:
        raise e
